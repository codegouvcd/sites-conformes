from sites_conformes.core.models import MegaMenu


def skiplinks(request) -> dict:
    return {
        "skiplinks": [
            {"link": "#content", "label": "Contenu"},
            # Cible renommee avec le portage de l en-tete vers le SDCD. Un lien
            # d evitement pointant dans le vide est pire que pas de lien : il est
            # le premier element atteint au clavier et ne mene nulle part.
            #
            # Limite connue, heritee de la conception amont a cible unique :
            # #sdcd-navigation est la navigation grand ecran, masquee sous 900 px.
            # Sur mobile ce lien reste donc sans effet ; le menu y est atteint par
            # son bouton, deux tabulations plus loin. Corriger demanderait deux
            # liens conditionnes au point de rupture.
            {"link": "#sdcd-navigation", "label": "Menu"},
        ]
    }


def mega_menus(request) -> dict:
    menus = list(MegaMenu.objects.all().values_list("parent_menu_item_id", flat=True))

    return {"mega_menus": menus}


def iframe(request) -> dict:
    return {"iframe": getattr(request, "iframe", False)}
