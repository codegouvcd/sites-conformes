# Modifications par rapport à l'amont

Ce fichier satisfait l'obligation de l'**AGPL-3.0 § 5 a)** : une version modifiée
doit porter mention bien visible du fait qu'elle a été modifiée, et de la date de
chaque modification.

**Amont :** [numerique-gouv/sites-conformes](https://github.com/numerique-gouv/sites-conformes)
**Base du fork :** v4.1.0, commit `1d36360`, 18 août 2026
**Auteur des modifications :** République Démocratique du Congo

Le détail commit par commit s'obtient par :

```bash
git fetch upstream && git log --oneline upstream/main..sdcd
```

---

## 2026-08-18 — Initialisation du fork

Aucune modification fonctionnelle. Mise en place seule.

| Fichier | Modification |
|---|---|
| `README.md` | Remplacé par le README du fork (origine, licence, contrainte DSFR, plan de portage) |
| `README.amont.md` | README d'origine conservé sous ce nom, pour attribution |
| `MODIFICATIONS.md` | Ajouté — ce fichier |

`LICENSE` est conservé à l'identique. Le code applicatif, les gabarits et les
dépendances sont inchangés.

---

## 2026-08-18 — Ajout de `django-sdcd`

Première brique de remplacement du DSFR. `django-dsfr` reste installé et les
gabarits du CMS n'ont pas encore été portés : les deux systèmes coexistent.

| Fichier | Modification |
|---|---|
| `sdcd/` | **Ajouté** — application Django du Système de design RDC |
| `config/settings.py` | `"sdcd"` ajouté à `INSTALLED_APPS`, à côté de `"dsfr"` |
| `verifier_sdcd.py` | **Ajouté** — rend les 14 tags et vérifie l'absence de classes `fr-*` |

### Contenu de l'application

- `sdcd/templatetags/sdcd_tags.py` — les **14 tags** que le CMS utilise, aux
  signatures identiques à celles de `django-dsfr` : le portage d'un gabarit se
  limite à remplacer le préfixe `dsfr_` par `sdcd_`.
- `sdcd/constants.py` — les 6 constantes référencées par les modèles Wagtail.
- `sdcd/forms.py` — `SdcdBaseForm`, `SdcdDjangoTemplates`, `SdcdBoundField`.
- `sdcd/utils.py` — `parse_tag_args`, `generate_pagination_list`,
  `sdcd_input_class_attr`.
- `sdcd/templates/sdcd/` — 13 gabarits + 5 fragments de formulaire.
- `sdcd/static/sdcd/` — feuilles du SDCD et script de bascule de thème.

### Vérifié

- Les 14 tags rendent sans erreur ; **aucune classe `fr-*`** dans la sortie.
- Les **41 classes émises existent toutes** dans les feuilles du SDCD
  (contrôle automatisé émises ∖ définies = ∅).
- Rendu réel dans un navigateur : **0 échec de contraste sur 37 nœuds**, en
  thème clair comme en thème sombre.
- L'application se charge dans le projet et `sdcd/alert.html` se résout.

### Écarts assumés

- Les widgets propres au DSFR (curseur numérique, contrôle segmenté, radio
  enrichie) n'ont pas d'équivalent SDCD : ils retombent sur le champ standard.
- `sdcd_favicon` référence des fichiers d'icône qui restent à produire.
- La transcription réutilise l'accordéon, faute de composant dédié au SDCD.

---

## 2026-08-18 — Remplacement de `django-dsfr` par `sdcd`

**`django-dsfr` est désinstallé et retiré des dépendances.** Le DSFR n'est plus
présent dans le projet, ni en code ni en feuilles de style — la contrainte
juridique est levée.

| Fichier | Modification |
|---|---|
| `pyproject.toml` | `django-dsfr` retiré ; `django-widget-tweaks` passé en dépendance directe (il n'était tiré que par django-dsfr, alors que le CMS l'utilise) |
| `uv.lock` | reverrouillé |
| `dsfr/` | **Ajouté** — couche d'alias vers `sdcd`, voir ci-dessous |
| `sdcd/templatetags/sdcd_tags.py` | complété à **40 tags**, parité entière avec l'amont |
| `sdcd/templates/sdcd/` | 22 gabarits ajoutés (36 au total + 5 fragments) |
| `sdcd/static/sdcd/compat-dsfr.css` | **Ajouté** — couche CSS transitoire `fr-*` |
| `verifier_sdcd.py` | étendu à quatre contrôles |

### Le choix : garder le nom `dsfr` comme alias

Le paquet `dsfr/` reprend le nom et l'API de django-dsfr et délègue tout à
`sdcd`. Les 55 gabarits qui écrivent `{% load dsfr_tags %}` et les 10 modules
qui importent `dsfr.constants` fonctionnent **sans une seule modification**.

Deux raisons de préférer l'alias au renommage massif :

1. Le renommage produirait un conflit à chaque reprise de l'amont ; l'alias
   nous laisse suivre `upstream/main` sans friction.
2. Il rend le basculement réversible et vérifiable d'un bloc, au lieu de 61
   modifications à relire une par une.

Aucune ligne du DSFR n'est reprise : seuls les noms le sont. Le balisage rendu
est celui du SDCD.

### Couche CSS transitoire

Les gabarits hérités écrivent 233 classes `fr-*` en dur. `compat-dsfr.css`
(2 610 règles) les rattache aux jetons du SDCD : **221 des 233 couvertes
(94 %)**. Les 12 restantes sont des préfixes de classes construites
dynamiquement (`fr-col-md-{{ n }}`, `fr-badge--{{ level }}`) dont les valeurs
produites à l'exécution sont, elles, couvertes.

Cette feuille est **transitoire** : chaque gabarit porté en `sdcd-*` permet d'en
retirer des règles.

### Vérifié — `python verifier_sdcd.py`, sortie 0

| Contrôle | Résultat |
|---|---|
| Tags `sdcd_*` rendus | **34/34**, aucune classe `fr-*` en sortie |
| Tags `dsfr_*` rendus via le shim | **34/34**, aucune classe `fr-*` |
| Alias `dsfr_france_connect` → CongoConnect | OK |
| Imports `dsfr.constants` / `forms` / `utils` | OK |
| Classes `sdcd-*` émises existant en feuille | **99/99** |
| Gabarits du CMS chargeant `dsfr_tags` | **55/55 compilés** |
| `manage.py check` | 0 erreur (9 avertissements Treebeard préexistants) |

### Écarts assumés

- Les widgets propres au DSFR (curseur numérique, contrôle segmenté, radio
  enrichie) retombent sur le champ standard.
- Les illustrations `fr-artwork-*` sont masquées faute d'équivalent.
- Les classes d'icônes `fr-icon-*` ne rendent rien : le SDCD emploie Remix Icon
  (`ri-*`). À traiter au portage des gabarits.
- `sdcd_favicon` référence des fichiers d'icône qui restent à produire.

---

## 2026-08-18 — Gabarits `dsfr/` etendus par chemin, et rendu de bout en bout

Le remplacement precedent etait incomplet : trois gabarits du CMS font
`{% extends "dsfr/… .html" %}` et surchargent des blocs nommes. Les tags ne
suffisaient donc pas — il fallait aussi les fichiers.

| Fichier | Modification |
|---|---|
| `dsfr/templates/dsfr/header.html` | **Ajouté** — en-tête d'État, blocs `brand`, `operator_logo`, `service_title`, `service_tagline`, `header_tools`, `header_search`, `burger_menu`, `main_menu` |
| `dsfr/templates/dsfr/footer.html` | **Ajouté** — blocs `footer_brand`, `brand`, `footer_description`, `footer_links`, `footer_bottom_extra` |
| `dsfr/templates/dsfr/follow.html` | **Ajouté** — blocs `follow_newsletter`, `follow_social` |
| `dsfr/templates/dsfr/form_snippet.html` | **Ajouté** — délègue à `sdcd/form_snippet.html` |

Les noms de blocs sont ceux de l'amont, pour que les surcharges du CMS
s'appliquent sans modification. Le balisage et la marque sont congolais :
armoiries de la République, filet tricolore, devise « Justice · Paix · Travail ».

### Rendu de bout en bout — enfin obtenu

Docker Desktop ne répond pas dans cet environnement ; la base a donc été montée
sur **SQLite**, application par application. À noter : `migrate` global échoue
sur SQLite (une migration emploie du SQL PostgreSQL) — **le CMS exige bien
PostgreSQL en exploitation**. Les applications nécessaires au rendu
(`wagtailcore`, `sites_conformes_core`, `sites_conformes_menus`, `wagtailmenus`,
`wagtailimages`, `wagtaildocs`, `taggit`) migrent, elles, sans difficulté.

| Gabarit réel du CMS | Rendu | Classes `sdcd-*` | Classes `fr-*` |
|---|---|---|---|
| `standalone.html` | 5 463 car. | 26 | 16 |
| `header.html` | 2 452 car. | 16 | 12 |
| `footer.html` | 1 675 car. | 14 | 5 |
| `follow.html` | 235 car. | 4 | 0 |
| `iframe.html` | 734 car. | 0 | 0 |

Les classes `fr-*` restantes proviennent du balisage propre au CMS ; la couche
`compat-dsfr.css` les habille — vérifié en navigateur sur `fr-logo`,
`fr-container` et `fr-btn`.

### Vérifié en navigateur, sur la sortie réelle

- Feuilles du SDCD chargées (`--sdcd-action: #00729A`), police **Inter**.
- **4 filets tricolores**, **2 armoiries de la République** — la marque d'État
  congolaise remplace bien la Marianne.
- **0 échec de contraste sur 14 nœuds de texte.**

---

## À venir

Les entrées suivantes seront ajoutées au fil du portage :

- portage progressif des gabarits vers `sdcd-*`, ce qui allégera d'autant
  `compat-dsfr.css` puis permettra de retirer l'alias `dsfr/` ;
- remplacement des classes d'icônes `fr-icon-*` par `ri-*` ;
- substitution de la marque d'État française par la marque congolaise ;
- production des fichiers d'icône référencés par `sdcd_favicon`.
