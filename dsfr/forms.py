"""Alias de la couche formulaires."""

from sdcd.forms import (  # noqa: F401
    SdcdBaseForm,
    SdcdBoundField,
    SdcdDjangoTemplates,
)

DsfrBaseForm = SdcdBaseForm
DsfrBoundField = SdcdBoundField
DsfrDjangoTemplates = SdcdDjangoTemplates

__all__ = ["DsfrBaseForm", "DsfrBoundField", "DsfrDjangoTemplates"]
