"""Petites fabriques de valeurs de blocs, pour que le contenu reste lisible.

Chaque fonction renvoie exactement la structure attendue par le bloc Wagtail
correspondant — noms de champs compris. Une valeur mal nommee n'est pas une
erreur pour Wagtail : elle est ignoree en silence, et le bloc se rend vide.
"""

from wagtail.rich_text import RichText


def rt(html):
    return RichText(html)


def img(image):
    """Valeur d'un ImageBlock (image, decorative, alt_text). Les images du site
    vitrine sont des compositions sans texte : decoratives, sans alternative."""
    return {"image": image, "decorative": True, "alt_text": ""}


def lien_page(page):
    return {"link_type": "page", "page": page}


def lien_externe(url):
    return {"link_type": "external_url", "external_url": url}


COTES = {"": "", "gauche": "sdcd-button--icone-gauche", "droite": "sdcd-button--icone-droite"}


def bouton(texte, page=None, url=None, type_="sdcd-button sdcd-button--primaire", icone="", cote=""):
    # icon_side attend la classe du systeme, pas le mot « gauche » : la valeur
    # brute etait refusee par le formulaire d'edition.
    valeur = {"text": texte, "button_type": type_, "icon_class": icone, "icon_side": COTES.get(cote, cote)}
    valeur.update(lien_page(page) if page is not None else lien_externe(url))
    return valeur


def tuile(titre, texte, page=None, url=None, image=None, badge=None, petite=False, niveau="h3", detail="",
          couleur_badge="info", horizontale=False):
    # Les couleurs de badge sont celles du systeme (succes, info, alerte,
    # erreur) ou d'illustration (chart-N) : « nouveau » n'en fait pas partie.
    valeur = {"title": titre, "heading_tag": niveau, "description": rt(texte), "is_small": petite,
              "is_horizontal": horizontale}
    if page is not None or url:
        valeur["link"] = lien_page(page) if page is not None else lien_externe(url)
    if image is not None:
        valeur["image"] = image
    if badge:
        valeur["top_detail_badges_tags"] = [("badges", [("badge", {"text": badge, "color": couleur_badge, "hide_icon": True})])]
    if detail:
        valeur["detail_text"] = detail
    return valeur


def carte(titre, texte, page=None, url=None, image=None, ratio="", etiquettes=(), detail_haut="", icone_haut="",
          niveau="h3", fond_gris=False, badge=None, couleur_badge="info", detail_bas="", appel=()):
    """Carte verticale ou horizontale : le ratio depend de la grille qui la recoit."""
    valeur = {
        "title": titre,
        "heading_tag": niveau,
        "description": rt(texte),
        "image_ratio": ratio,
        "grey_background": fond_gris,
    }
    if page is not None or url:
        valeur["link"] = lien_page(page) if page is not None else lien_externe(url)
    if image is not None:
        valeur["image"] = img(image)
    if etiquettes:
        valeur["top_detail_badges_tags"] = [
            ("tags", [("tag", {"label": e, "is_small": True, "color": "chart-1"}) for e in etiquettes])
        ]
    elif badge:
        valeur["top_detail_badges_tags"] = [("badges", [("badge", {"text": badge, "color": couleur_badge, "hide_icon": True})])]
    if detail_haut:
        valeur["top_detail_text"] = detail_haut
        valeur["top_detail_icon"] = icone_haut
    if detail_bas:
        valeur["bottom_detail_text"] = detail_bas
    if appel:
        valeur["call_to_action"] = [("buttons", [("button", b) for b in appel])]
    return valeur


def carte_horizontale(titre, texte, **options):
    """Carte seule sur sa ligne (bloc « card ») ; `ratio` : sdcd-card--horizontal-tiers ou -moitie."""
    return ("card", carte(titre, texte, **options))


def image_centree(image, legende="", alt="", largeur="", ratio=""):
    return ("image", {"title": "", "heading_tag": "h3", "image": image, "alt": alt, "width": largeur,
                      "image_ratio": ratio, "caption": legende, "url": ""})


def lien_simple(texte, page=None, url=None, icone="", taille=""):
    valeur = {"text": texte, "icon": icone, "size": taille}
    valeur.update(lien_page(page) if page is not None else lien_externe(url))
    return ("link", valeur)


def separateur(haut=3, bas=3):
    return ("separator", {"top_margin": haut, "bottom_margin": bas})


def ancre(identifiant):
    return ("anchor", {"anchor_id": identifiant})


def texte_appel(html, boutons_):
    return ("text_cta", {"text": rt(html), "cta_buttons": [("buttons", [("button", b) for b in boutons_])]})


def fond_menu_lateral(contenu, titre_menu, page_racine, couleur="gris", haut=5, bas=5):
    """Fond pleine largeur avec, a gauche, l'arbre des pages sous `page_racine`."""
    return ("fullwidthbackgroundwithsidemenu", {
        "bg_color_class": couleur, "top_margin": haut, "bottom_margin": bas,
        "main_content": contenu, "sidemenu_title": titre_menu,
        "sidemenu_content": [("pagetree", {"page": page_racine})],
    })


def grille(items, largeur="4", horizontal="left", vertical=""):
    """`items` : liste de ("tile"|"card", valeur)."""
    return ("item_grid", {"column_width": largeur, "horizontal_align": horizontal, "vertical_align": vertical, "items": items})


def paragraphe(html):
    return ("paragraph", rt(html))


def fond(contenu, couleur="bleu", haut=5, bas=5, image=None):
    """Bloc pleine largeur. Dans ce bloc, le texte riche s'appelle `text`."""
    valeur = {"bg_color_class": couleur, "top_margin": haut, "bottom_margin": bas, "content": contenu}
    if image is not None:
        valeur["bg_image"] = image
    return ("fullwidthbackground", valeur)


def encadre(titre, html, icone="ri-information-line", couleur="chart-1", niveau="h2", bouton_=None):
    valeur = {"title": titre, "heading_tag": niveau, "icon_class": icone, "text": rt(html), "color": couleur}
    if bouton_:
        valeur["button"] = bouton_
    return ("callout", valeur)


def accordeons(titre, entrees, niveau="h2"):
    """AccordionsBlock est un StreamBlock (un titre, puis des accordeons), pas
    un StructBlock : sa valeur est une liste de couples."""
    return ("accordions", [("title", titre)] + [("accordion", {"title": t, "content": rt(c)}) for t, c in entrees])


def etapier(titre, total, courante, etapes, niveau="h2"):
    return ("stepper", {"title": titre, "heading_tag": niveau, "total": total, "current": courante,
                        "steps": [("step", {"title": t, "detail": d}) for t, d in etapes]})


def citation(texte, auteur, role, image=None, couleur="chart-1"):
    """La couleur d'une citation vient de la palette d'illustration (chart-N)."""
    valeur = {"quote": texte, "author_name": auteur, "author_title": role, "color": couleur}
    if image is not None:
        valeur["image"] = image
    return ("quote", valeur)


def mise_en_avant(html, couleur="chart-1", taille=""):
    return ("highlight", {"text": rt(html), "color": couleur, "size": taille})


def alerte(titre, texte, niveau_="info", tag="h3"):
    """`description` est un TextBlock : du texte brut, sans balise."""
    import re

    return ("alert", {"title": titre, "description": re.sub(r"<[^>]+>", "", texte), "level": niveau_, "heading_tag": tag})


def badges(*textes, couleur="info"):
    return ("badges_list", [("badge", {"text": t, "color": couleur, "hide_icon": True}) for t in textes])


def etiquettes(*libelles, couleur="chart-1"):
    return ("tags_list", [("tag", {"label": t, "is_small": False, "color": couleur}) for t in libelles])


def boutons(*boutons_, position=""):
    return ("buttons_list", {"buttons": [("button", b) for b in boutons_], "position": position})


def image_texte(image, html, cote="right", largeur="4", lien=None):
    valeur = {"image": img(image), "image_side": cote, "image_ratio": largeur, "text": rt(html)}
    if lien:
        valeur["link"] = lien
    return ("imageandtext", valeur)


def onglets(*onglets_):
    """`onglets_` : (titre, [blocs de colonne])."""
    return ("tabs", [("tabs", {"title": t, "content": c}) for t, c in onglets_])


def colonnes(titre, colonnes_, couleur="", niveau="h2", haut=5, bas=5):
    """`colonnes_` : liste de (largeur, [blocs])."""
    return ("multicolumns", {
        "bg_color_class": couleur, "title": titre, "heading_tag": niveau,
        "top_margin": haut, "bottom_margin": bas,
        "columns": [("column", {"width": l, "content": c}) for l, c in colonnes_],
    })


def fiche_contact(nom, role, organisation, infos, image=None, etiquettes_=()):
    # contact_info est un CharBlock : une chaine, pas un RichText — un objet
    # RichText dans un CharBlock n'est pas serialisable en JSON et faisait
    # echouer l'enregistrement de la page entiere.
    valeur = {"heading_tag": "h3", "name": nom, "role": role, "organization": organisation,
              "contact_info": infos}
    if image is not None:
        valeur["image"] = image
    if etiquettes_:
        valeur["tags"] = [("tag", {"label": e, "is_small": True, "color": "chart-1"}) for e in etiquettes_]
    return ("contact_card", valeur)


def actualites_recentes(blog, titre="Les actualités à la une", nombre=4):
    return ("blog_recent_entries", {"title": titre, "heading_tag": "h2", "blog": blog, "entries_count": nombre})


def evenements_recents(agenda, titre="Prochains rendez-vous", nombre=3):
    return ("events_recent_entries", {"title": titre, "heading_tag": "h2", "index_page": agenda, "entries_count": nombre})


def hero_image_texte(titre, sous_titre, boutons_, image, position="left", fond_="", haut=0, bas=0):
    return ("hero_text_image", {
        "text_content": {"hero_title": titre, "hero_subtitle": rt(sous_titre), "position": position},
        "buttons": boutons_,
        "image": img(image),
        "layout": {"top_margin": haut, "bottom_margin": bas, "background_color": fond_},
    })


def hero_fond_image(titre, sous_titre, boutons_, image, masque="darken", position=""):
    return ("hero_text_background_image", {
        "text_content": {"hero_title": titre, "hero_subtitle": rt(sous_titre), "position": position},
        "buttons": boutons_,
        "background_color_or_image": "image",
        "image": {"image": img(image), "image_positioning": "", "image_mask": masque},
        "background_color": "",
    })


def hero_bandeau(titre, sous_titre, boutons_, image, position="bottom", fond_="", haut=0, bas=0, cadrage=""):
    """`cadrage` : partie de l'image gardee dans le bandeau 32:9 ("" = centre)."""
    return ("hero_text_wide_image", {
        "text_content": {"hero_title": titre, "hero_subtitle": rt(sous_titre), "position": position},
        "layout": {"top_margin": haut, "bottom_margin": bas, "background_color": fond_},
        "buttons": boutons_,
        "image": {"image": img(image), "image_positioning": cadrage, "image_width": "sdcd-media--lg",
                  "image_ratio": "sdcd-ratio-32x9"},
    })
