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
