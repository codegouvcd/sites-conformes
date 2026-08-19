"""Alias des utilitaires."""

from sdcd.utils import (  # noqa: F401
    generate_pagination_list,
    lazy_static,
    parse_tag_args,
    sdcd_input_class_attr,
)

dsfr_input_class_attr = sdcd_input_class_attr
generate_summary_items = generate_pagination_list  # nom historique côté DSFR

__all__ = [
    "dsfr_input_class_attr",
    "parse_tag_args",
    "generate_pagination_list",
    "lazy_static",
]
