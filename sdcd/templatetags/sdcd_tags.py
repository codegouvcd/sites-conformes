"""
Tags de gabarit du Système de design RDC.

Miroir de `dsfr_tags` restreint aux 14 tags que le CMS emploie réellement.
Les signatures sont identiques à celles de django-dsfr : le portage d'un
gabarit se limite à remplacer le préfixe `dsfr_` par `sdcd_`.
"""

from django import template
from django.core.paginator import Page
from django.template.context import Context
from django.utils.html import format_html

from sdcd.utils import generate_pagination_list, parse_tag_args

register = template.Library()


# ---------------------------------------------------------------- socle

@register.inclusion_tag("sdcd/global_css.html")
def sdcd_css() -> dict:
    """Feuille de style du système. À placer dans le `<head>`."""
    return {}


@register.inclusion_tag("sdcd/global_js.html", takes_context=True)
def sdcd_js(context, *args, **kwargs) -> dict:
    """Scripts du système. `nonce` est repris pour la politique CSP."""
    return {"nonce": kwargs.get("nonce", "")}


@register.inclusion_tag("sdcd/favicon.html")
def sdcd_favicon() -> dict:
    return {}


@register.inclusion_tag("sdcd/theme_modale.html")
def sdcd_theme_modale() -> dict:
    """Boîte de dialogue de choix du thème clair/sombre/système."""
    return {}


# ---------------------------------------------------------------- composants

@register.inclusion_tag("sdcd/accordion.html")
def sdcd_accordion(*args, **kwargs) -> dict:
    """
    Accordéon. Clés : `id`, `title`, `content`, `heading_tag`, `extra_classes`.
    """
    allowed_keys = ["id", "title", "content", "heading_tag", "extra_classes"]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/alert.html")
def sdcd_alert(*args, **kwargs) -> dict:
    """
    Message d'alerte. Clés : `title`, `type` (info, succes, alerte, erreur),
    `content`, `heading_tag`, `is_collapsible`, `id`, `extra_classes`.
    """
    allowed_keys = [
        "title", "type", "content", "heading_tag",
        "is_collapsible", "id", "extra_classes",
    ]
    tag_data = parse_tag_args(args, kwargs, allowed_keys)
    # Le DSFR nomme « warning » ce que le SDCD nomme « alerte ».
    equivalences = {"warning": "alerte", "error": "erreur", "success": "succes"}
    if tag_data.get("type") in equivalences:
        tag_data["type"] = equivalences[tag_data["type"]]
    return {"self": tag_data}


@register.inclusion_tag("sdcd/breadcrumb.html", takes_context=True)
def sdcd_breadcrumb(context: Context, tag_data: dict | None = None) -> dict:
    """
    Fil d'Ariane. Clés : `links` (liste de dicts `url`/`title`), `current`,
    `root_dir`. À défaut d'argument, la valeur est prise dans le contexte.
    """
    if tag_data is None:
        tag_data = context.get("breadcrumb_data", {})
    tag_data = dict(tag_data)
    tag_data.setdefault("id", "sdcd-breadcrumb")
    return {"self": tag_data}


@register.inclusion_tag("sdcd/notice.html")
def sdcd_notice(*args, **kwargs) -> dict:
    """
    Bandeau d'information haut de page. Clés : `title`, `description`, `link`,
    `type`, `icon`, `is_collapsible`.
    """
    allowed_keys = [
        "title", "description", "link", "type", "icon",
        "is_collapsible", "extra_classes",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/pagination.html", takes_context=True)
def sdcd_pagination(context: Context, page_obj: Page) -> dict:
    """Pagination. Prend l'objet `Page` fourni par le paginateur Django."""
    return {"request": context.get("request"), "page_obj": generate_pagination_list(page_obj)}


@register.inclusion_tag("sdcd/quote.html")
def sdcd_quote(*args, **kwargs) -> dict:
    """
    Citation. Clés : `text`, `author`, `source`, `source_url`, `image_url`,
    `extra_classes`.
    """
    allowed_keys = [
        "text", "author", "source", "source_url", "image_url", "extra_classes",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/skiplinks.html", takes_context=True)
def sdcd_skiplinks(context: Context, items: list | None = None) -> dict:
    """Liens d'évitement. `items` : liste de dicts `link`/`label`."""
    if items is None:
        items = context.get("skiplinks", [])
    return {"self": {"items": items}}


@register.inclusion_tag("sdcd/transcription.html")
def sdcd_transcription(*args, **kwargs) -> dict:
    """Transcription textuelle d'un média. Clés : `title`, `content`, `id`."""
    allowed_keys = ["title", "content", "id", "extra_classes"]
    tag_data = parse_tag_args(args, kwargs, allowed_keys)
    tag_data.setdefault("id", "transcription")
    return {"self": tag_data}


@register.inclusion_tag("sdcd/django_messages.html", takes_context=True)
def sdcd_django_messages(
    context, is_collapsible=False, extra_classes=None, wrapper_classes=None
) -> dict:
    """Rend les messages Django sous forme d'alertes du système."""
    return {
        "messages": context.get("messages", []),
        "is_collapsible": is_collapsible,
        "extra_classes": extra_classes or "",
        "wrapper_classes": wrapper_classes or "sdcd-container sdcd-my-4",
    }


# ---------------------------------------------------------------- formulaires

@register.simple_tag
def sdcd_form_field(field) -> str:
    """Rend un champ de formulaire avec son étiquette, son aide et ses erreurs."""
    if field is None:
        return ""
    return field.as_field_group()


@register.simple_tag
def sdcd_mark_optionnal_fields(bf):
    """
    Rend « (facultatif) » après l'étiquette d'un champ non requis, si le réglage
    `SDCD_MARK_OPTIONAL_FIELDS` est actif. Ne rend que le suffixe : l'étiquette
    est écrite par le gabarit appelant.
    """
    from django.conf import settings

    if bf.field.required or not getattr(settings, "SDCD_MARK_OPTIONAL_FIELDS", False):
        return ""
    return format_html(' <span class="sdcd-texte-muet">(facultatif)</span>')


@register.filter
def sdcd_input_class_attr(bf):
    """Pose les classes du système sur le champ, puis le rend."""
    from sdcd.utils import sdcd_input_class_attr as _appliquer

    return _appliquer(bf)


# ---------------------------------------------------------------- interne

@register.simple_tag(takes_context=True)
def url_remplace_params(context, **kwargs):
    """
    Reconstruit la chaîne de requête en remplaçant les paramètres fournis.
    Utilisé par la pagination pour conserver les filtres actifs.
    """
    request = context.get("request")
    if request is None:
        return "&".join(f"{k}={v}" for k, v in kwargs.items())
    query = request.GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


# ================================================================
# Parité d'API avec django-dsfr
# Les tags ci-dessous ne sont pas employés par le CMS, mais un remplacement
# « plug and play » exige que toute la surface existe.
# ================================================================

@register.inclusion_tag("sdcd/badge.html")
def sdcd_badge(*args, **kwargs) -> dict:
    """Badge. Clés : `label`, `extra_classes`."""
    return {"self": parse_tag_args(args, kwargs, ["label", "extra_classes"])}


@register.inclusion_tag("sdcd/badge_group.html")
def sdcd_badge_group(items: list) -> dict:
    return {"self": {"items": items}}


@register.inclusion_tag("sdcd/button.html")
def sdcd_button(*args, **kwargs) -> dict:
    """
    Bouton. Clés : `label`, `name`, `type` (primaire, secondaire, tertiaire),
    `onclick`, `is_disabled`, `extra_classes`.
    """
    allowed_keys = ["label", "name", "type", "onclick", "is_disabled", "extra_classes"]
    tag_data = parse_tag_args(args, kwargs, allowed_keys)
    # Le DSFR met le type HTML dans `type` et la variante dans les classes ;
    # le SDCD range la variante dans `type`. On accepte les deux écritures.
    if tag_data.get("type") in ("submit", "button", "reset"):
        tag_data["html_type"] = tag_data.pop("type")
    return {"self": tag_data}


@register.inclusion_tag("sdcd/button_group.html")
def sdcd_button_group(*args, **kwargs) -> dict:
    return {"self": parse_tag_args(args, kwargs, ["items", "extra_classes"])}


@register.inclusion_tag("sdcd/callout.html")
def sdcd_callout(*args, **kwargs) -> dict:
    """Mise en avant. Clés : `text`, `title`, `heading_tag`, `icon_class`, `button`."""
    allowed_keys = ["text", "title", "heading_tag", "icon_class", "extra_classes", "button"]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/card.html")
def sdcd_card(*args, **kwargs) -> dict:
    """Carte de contenu. Voir le composant `Card` du SDCD."""
    allowed_keys = [
        "title", "heading_tag", "description", "image_url", "image_alt",
        "ratio_class", "media_badges", "new_tab", "link", "enlarge_link",
        "extra_classes", "top_detail", "bottom_detail", "call_to_action", "id",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/consent.html")
def sdcd_consent(*args, **kwargs) -> dict:
    """Bandeau de consentement aux témoins de connexion."""
    return {"self": parse_tag_args(args, kwargs, ["title", "content"])}


@register.inclusion_tag("sdcd/content.html")
def sdcd_content(*args, **kwargs) -> dict:
    """Média avec légende et transcription."""
    allowed_keys = [
        "image_url", "iframe_url", "svg", "caption", "alt_text",
        "extra_classes", "ratio_class", "transcription",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/connect.html")
def sdcd_connect(*args, **kwargs) -> dict:
    """
    Bouton d'identité numérique **CongoConnect**.

    Remplace `dsfr_france_connect` : l'alias rend ce composant, la fédération
    d'identité congolaise n'étant pas FranceConnect.
    """
    return {"self": parse_tag_args(args, kwargs, ["id", "plus", "service"])}


@register.inclusion_tag("sdcd/highlight.html")
def sdcd_highlight(*args, **kwargs) -> dict:
    """Citation en exergue. Clés : `content`, `size_class`, `extra_classes`."""
    return {"self": parse_tag_args(args, kwargs, ["content", "size_class", "extra_classes"])}


@register.inclusion_tag("sdcd/input.html")
def sdcd_input(*args, **kwargs) -> dict:
    """Champ de saisie autonome, hors formulaire Django."""
    allowed_keys = ["id", "label", "type", "onchange", "value", "min", "max", "extra_classes"]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/link.html")
def sdcd_link(*args, **kwargs) -> dict:
    """Lien. Clés : `url`, `label`, `is_external`, `extra_classes`."""
    return {"self": parse_tag_args(args, kwargs, ["url", "label", "is_external", "extra_classes"])}


@register.inclusion_tag("sdcd/select.html")
def sdcd_select(*args, **kwargs) -> dict:
    """Liste déroulante autonome."""
    allowed_keys = [
        "id", "label", "hint", "onchange", "selected", "default", "options", "extra_classes",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/sidemenu.html", takes_context=True)
def sdcd_sidemenu(context: Context, *args, **kwargs) -> dict:
    """Menu latéral. Marque l'entrée courante à partir du chemin demandé."""
    allowed_keys = ["title", "button_label", "items", "heading_tag", "extra_classes", "id"]
    tag_data = parse_tag_args(args, kwargs, allowed_keys)
    request = context.get("request")
    tag_data["chemin_actif"] = request.path if request is not None else ""
    return {"self": tag_data}


@register.inclusion_tag("sdcd/stepper.html")
def sdcd_stepper(*args, **kwargs) -> dict:
    """Indicateur d'étapes."""
    allowed_keys = [
        "current_step_id", "current_step_title", "next_step_title",
        "total_steps", "heading_tag",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/summary.html")
def sdcd_summary(items: list, heading_tag: str = "p", summary_id: str = "") -> dict:
    """Sommaire d'article."""
    return {"self": {"items": items, "heading_tag": heading_tag, "id": summary_id}}


@register.inclusion_tag("sdcd/table.html")
def sdcd_table(*args, **kwargs) -> dict:
    """Tableau. Clés : `caption`, `header`, `content`, `extra_classes`."""
    allowed_keys = ["caption", "content", "header", "extra_classes"]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/tag.html")
def sdcd_tag(*args, **kwargs) -> dict:
    """Étiquette. Clés : `label`, `link`, `is_selectable`, `is_selected`, `is_dismissable`."""
    allowed_keys = [
        "label", "link", "onclick", "extra_classes",
        "is_selectable", "is_selected", "is_dismissable",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/tile.html")
def sdcd_tile(*args, **kwargs) -> dict:
    """Tuile de service."""
    allowed_keys = [
        "title", "url", "image_path", "svg_path", "description", "detail",
        "top_detail", "heading_tag", "id", "enlarge_link", "extra_classes",
    ]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/toggle.html")
def sdcd_toggle(*args, **kwargs) -> dict:
    """Interrupteur."""
    allowed_keys = ["label", "name", "help_text", "is_disabled", "is_checked",
                    "extra_classes", "id"]
    return {"self": parse_tag_args(args, kwargs, allowed_keys)}


@register.inclusion_tag("sdcd/tooltip.html")
def sdcd_tooltip(*args, **kwargs) -> dict:
    """Infobulle. Clés : `content`, `label`, `is_clickable`, `id`."""
    return {"self": parse_tag_args(args, kwargs, ["content", "label", "is_clickable", "id"])}


@register.inclusion_tag("sdcd/accordion_group.html")
def sdcd_accordion_group(items: list) -> dict:
    """Groupe d'accordéons : un conteneur, plusieurs volets."""
    return {"self": {"items": items}}


@register.simple_tag
def sdcd_form(form) -> str:
    """Rend un formulaire complet."""
    return form.render() if hasattr(form, "render") else str(form)


# ---------------------------------------------------------------- filtres

@register.filter
def sdcd_inline(field):
    """Passe un groupe de cases ou de boutons radio en disposition horizontale."""
    if hasattr(field, "field") and hasattr(field.field, "widget"):
        classe = field.field.widget.attrs.get("class", "")
        field.field.widget.attrs["class"] = (classe + " sdcd-flex sdcd-wrap").strip()
    return field


@register.filter
def concatenate(valeur, arg):
    """Concatène deux chaînes."""
    return f"{valeur}{arg}"


@register.filter
def hyphenate(valeur, arg):
    """Joint deux valeurs par un trait d'union, en ignorant les vides."""
    morceaux = [str(v) for v in (valeur, arg) if v not in (None, "")]
    return "-".join(morceaux)


@register.filter
def strfmt(valeur, gabarit):
    """Applique un gabarit de formatage, `{}` marquant la valeur."""
    return gabarit.format(valeur)
