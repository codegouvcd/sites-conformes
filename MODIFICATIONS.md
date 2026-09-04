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

## 2026-08-19 — SDCD 0.6.0 : comportements et auto-hebergement

Reprise du systeme de design en version 0.6.0. Deux consequences pour le CMS.

| Fichier | Modification |
|---|---|
| `sdcd/static/sdcd/sdcd.js` | Remplace le script de bascule de theme par la couche complete : 14 comportements, 385 lignes |
| `sdcd/static/sdcd/assets/fontes/` | **Ajoute** — 7 fichiers woff2, 548 Ko |
| `sdcd/static/sdcd/assets/fonts.css` | Faces locales, plus aucune requete vers Google Fonts |
| `sdcd/static/sdcd/assets/icones.css` | **Ajoute** — glyphes Remix Icon, plus aucune requete vers jsDelivr |
| `sdcd/templates/sdcd/toggle.html` | **Corrige** — rendait une case a cocher la ou le CSS attend `aria-checked` |

### Ce que cela change pour le deploiement

Le site ne depend plus d'aucun domaine tiers pour ses fontes et ses icones :
ni fuite d'adresse IP des usagers vers un hebergeur etranger, ni dependance a
une liaison internationale. Le poids statique du paquet passe a 1,3 Mo, servi
depuis le meme domaine.

### Verifie

- `verifier_sdcd.py` : aucun defaut, 55/55 gabarits compiles.
- Aucune reference `fonts.googleapis` ou `jsdelivr` dans les feuilles servies.

---

## 2026-08-19 — SDCD 0.9.0 : audit et corrections de securite

| Fichier | Modification |
|---|---|
| `sdcd/static/sdcd/*` | Reprise de la distribution 0.9.0 |
| `sdcd/templates/sdcd/alert.html`, `notice.html`, `theme_modale.html` | `onclick` en ligne remplace par `data-sdcd-fermer-parent` / `data-sdcd-ferme` |
| `sdcd/templates/sdcd/button.html`, `tag.html`, `button_group.html` | **Parametre `onclick` retire de l'API** |

### Pourquoi

Un `onclick` en ligne impose `unsafe-inline` dans la politique de securite de
contenu, c'est-a-dire renoncer a la protection principale contre l'injection
de script. Et le parametre `onclick` de `sdcd_button` injectait du JavaScript
arbitraire dans un attribut : des lors que sa valeur venait du CMS, un
redacteur pouvait executer du script chez les visiteurs. L'echappement de
Django empechait la sortie de l'attribut, pas l'execution de son contenu.

**Rupture d'API assumee** : `{% sdcd_button onclick="…" %}` ne fait plus rien.
Aucun gabarit du CMS ne l'employait.

### A traiter cote CMS

Les gabarits referencent `request.csp_nonce`, mais **aucun middleware CSP
n'est installe** : `django-csp` n'est pas une dependance et le nonce se
resout a vide. Le site n'a donc aujourd'hui **aucune politique de securite de
contenu**. Le SDCD est desormais compatible avec une CSP stricte ; l'activer
releve du CMS.

### Verifie

`verifier_sdcd.py` : aucun defaut, 55/55 gabarits compiles.

---

## 2026-08-30 — Premier deploiement : chevron DSFR residuel

| Fichier | Modification |
|---|---|
| `sites_conformes/static/css/style.css` | 3 `url()` vers `dsfr/dist/icons/arrows/arrow-down-s-line.svg` remplacees par un `data:` URI |
| `verifier_sdcd.py` | Nouveau controle 5 : references `url()` mortes |

### Ce qui s'est passe

Le premier deploiement a **boucle en redemarrage**, exit 1 repete. Cause :

```
whitenoise.storage.MissingFileError: The file
'dsfr/dist/icons/arrows/arrow-down-s-line.svg' could not be found
```

En production, `SF_USE_WHITENOISE=1` active `CompressedManifestStaticFilesStorage`,
qui **resout chaque `url()`** au moment de `collectstatic` et leve une erreur fatale
sur une reference morte. `just deploy` echouait donc avant `gunicorn`, et le
conteneur mourait en boucle.

Le chevron etait le dernier vestige du DSFR dans les feuilles de style. Mes controles
precedents portaient sur les *fichiers* DSFR collectes — aucun ne restait — mais pas
sur les *references* pointant vers eux depuis un CSS.

### Pourquoi un `data:` URI plutot qu'un fichier SDCD

Un fichier de remplacement aurait recree la meme dependance, donc le meme mode de
panne. Le chevron est integre au CSS : plus aucun fichier a resoudre.

Les deux premieres occurrences sont des `mask-image`, la troisieme vit dans un
`@media (min-width:0 )` — un hack IE, code mort pour tout navigateur moderne, mais
que `collectstatic` analyse quand meme.

### Controle ajoute

Le controle 5 parcourt les `url()` de toutes les feuilles sous
`sites_conformes/static` et echoue si l'une pointe dans le vide. **Teste a l'envers** :
une reference fantome injectee le fait passer en defaut, son retrait le remet au vert.

### Deuxieme tour : quatre vestiges DSFR de plus

`collectstatic` passait, mais `create_starter_pages` tombait sur :

```
FileNotFoundError: 'staticfiles/dsfr/dist/artwork/pictograms/'
```

Un balayage de tout le code Python a revele **quatre** references DSFR mortes, pas
une. Les trois autres n'auraient pas fait tomber le deploiement : elles auraient
casse l'administration a l'usage.

| Fichier | Reference morte | Consequence si non corrigee |
|---|---|---|
| `core/management/commands/import_dsfr_pictograms.py` | `os.listdir` sur les pictogrammes | **Conteneur en boucle** |
| `core/widgets.py` | `dsfr/dist/utility/utility.min.css` et le JS du selecteur d'icones | **500 sur toute page d'edition a champ d'icone** |
| `dashboard/wagtail_hooks.py` | `static("dsfr/dist/component/notice/notice.min.css")` | **500 sur toute page d'administration** |
| `config/urls.py` | favicon DSFR | 404 sur `/favicon.ico` |

Les deux 500 viennent du meme mecanisme que le chevron : `ManifestStaticFilesStorage`
leve une exception quand `static()` vise un fichier absent — au rendu cette fois,
pas a la collecte.

**Decisions prises**

- *Pictogrammes* : import ignore proprement si le repertoire est absent. Ce sont les
  pictogrammes de l'Etat francais ; le portage devait les retirer, il n'y a rien a
  importer. Les reintroduire aurait ete fautif au-dela de la technique.
- *Selecteur d'icones* : la bibliotheque venait de `django-dsfr`, desinstalle. Le
  widget redevient un champ texte ou le rediger saisit la classe. **Regression
  d'ergonomie assumee**, preferable a un 500.
- *Notice d'administration* : le lien mort est retire sans remplacement.
  `components.css` du SDCD vise le site public et deborderait sur le back-office —
  ce que le commentaire d'origine cherchait deja a eviter. Les notices perdent leur
  fond colore, rien de plus.
- *Favicon* : pointe desormais sur les **armoiries de la RDC**.

`manage.py check` : 0 erreur, 9 avertissements `treebeard.E001` preexistants.

### Troisieme tour : cinq references statiques mortes dans les gabarits

Le conteneur tenait enfin debout, mais chaque page renvoyait 500 :

```
ValueError: Missing staticfiles manifest entry for 'sdcd/favicon/favicon.svg'
```

Meme mecanisme que les fois precedentes, dans les gabarits cette fois — ce qu'un
balayage du code Python ne pouvait pas voir.

| Reference morte | Origine |
|---|---|
| `sdcd/favicon/favicon.svg` | **Notre portage** : `favicon.html` pointait trois fichiers jamais crees |
| `sdcd/favicon/favicon.ico` | idem |
| `sdcd/favicon/apple-touch-icon.png` | idem |
| `dsfr/dist/artwork/pictograms/digital/search.svg` | Vestige DSFR |
| `dsfr/dist/artwork/pictograms/digital/calendar.svg` | Vestige DSFR |

Le favicon etait le plus grave : `favicon.html` est inclus par le gabarit de base,
donc **tout le site** renvoyait 500, pas seulement une page.

**Pieces creees plutot que references supprimees**

- `sdcd/static/sdcd/favicon/favicon.svg` — drapeau national simplifie, lisible a 16 px
- `sdcd/static/sdcd/pictogrammes/recherche.svg`
- `sdcd/static/sdcd/pictogrammes/calendrier.svg`

Les pictogrammes sont decoratifs (`alt=""`). Les supprimer aurait laisse des colonnes
vides dans deux mises en page ; les redessiner aux couleurs du SDCD preserve la
composition et amorce un jeu de pictogrammes propre au systeme.

Pas de `favicon.ico` : un `.ico` ne s'ecrit pas a la main, et il est inutile des lors
qu'une icone SVG est declaree. L'icone Apple reutilise les armoiries.

### Controle 6 ajoute

Il interroge les **finders de Django** — ceux que `static()` consulte reellement —
plutot que de parcourir les repertoires a la main. Mon premier balayage, artisanal,
produisait trois faux positifs sur des statiques fournis par les applications
installees (`wagtail_honeypot`, l'application `events`). **Teste a l'envers.**

### Quatrieme tour : commentaires Django rendus aux visiteurs

Signale par l'utilisateur depuis le site en ligne : le texte de plusieurs
commentaires s'affichait **en haut de chaque page**.

Cause : en Django, `{# ... #}` ne vaut que sur **une seule ligne**. Des qu'il en
couvre plusieurs, le moteur cesse de le reconnaitre et le rend litteralement. Cinq
commentaires ecrits pendant le portage etaient dans ce cas, dont ceux de
`favicon.html` et `global_css.html`, inclus par le gabarit de base — donc visibles
partout.

| Gabarit | |
|---|---|
| `sdcd/favicon.html` | **Notre portage** |
| `sdcd/global_css.html` | idem |
| `sdcd/theme_modale.html` | idem |
| `sdcd/toggle.html` | idem |
| `dsfr/header.html` | idem |
| `demo/annuaire/.../liste_psychologues.html` | amont |

Les six sont convertis en `{% comment %}`, seule forme valide sur plusieurs lignes.

**Controle 7 ajoute**, teste a l'envers. Aucun des six controles precedents ne
pouvait voir ce defaut : les gabarits *compilaient* sans erreur et toutes les
references statiques *resolvaient*. Seul un regard sur la page rendue le revelait —
ce qui est exactement ce que l'utilisateur a fait.

### Cinquieme tour : l'en-tete n'etait pas au SDCD

Signale par l'utilisateur — « le modele de site ne semble pas 100 % conforme ».
Mesure faite plutot que discutee, sur la page rendue.

**Etat initial** : 51 % des classes de la page d'accueil etaient encore `fr-*`,
et **neuf classes n'avaient aucune regle**, donc s'affichaient sans style.

Parmi elles, **sept `sdcd-header__*` inventees** par le portage : `__bloc`,
`__lien-marque`, `__marque`, `__mention`, `__navigation`, `__outils`,
`__utilitaire`. Aucune n'existe dans le systeme de design. L'en-tete s'affichait
donc en vrac — armoiries, titre et bouton empiles verticalement — et le bouton
« Fermer » du menu mobile restait visible en permanence.

C'est la **troisieme fois** que ce portage invente des noms de classes au lieu de
lire l'API. Le controle 3 existait pour cela, mais ne parcourait que
`sdcd/templates/` : l'en-tete vit dans `dsfr/templates/`, le shim d'alias, et lui
echappait entierement. Il examine desormais **tous** les gabarits suivis — 141
classes au lieu de 99.

**Trois defauts du SDCD lui-meme, decouverts par ce portage**

| Version | Defaut |
|---|---|
| 0.9.1 | Le bouton de menu de l'en-tete n'avait **aucun comportement** dans la couche JavaScript autonome. `Header.jsx` gere cet etat en React ; Django, WordPress et FastAPI n'avaient rien, donc **le menu ne s'ouvrait pas sur mobile**. |
| 0.9.2 | `hidden` ne masquait pas : sa regle navigateur a la specificite la plus faible et toute classe fixant `display` la supplantait. Touchait les **huit** points d'appel de `afficher()`. |
| 0.9.3 | La garde 0.9.2 ne suffisait pas — a `!important` egal, `[hidden]` et `.sdcd-mobile-only` valent toutes deux 0-1-0, l'ordre des feuilles decidait. Selecteur double, `[hidden][hidden]`. |

Le 0.9.2 illustre le risque de conclure trop vite : j'avais annonce la correction
avant de la verifier sur le site, et elle etait insuffisante.

**Resultat mesure sur la page d'accueil**

| | Avant | Apres |
|---|---|---|
| Classes `sdcd-*` | 27 | **38** |
| Classes `fr-*` | 31 | 23 |
| `sdcd-*` sans regle | 7 | **0** |
| `fr-*` sans regle | 5 | **0** |

Menu mobile verifie dans un vrai navigateur : ouverture, permutation d'icone,
fermeture.

**Ce qui reste**

Sur les 163 gabarits, **252 classes `fr-*` sont emises, 200 couvertes, 52 sans
regle** (20 %). Elles concernent des pages non rendues lors de ce controle :
index de blog, pages protegees par mot de passe, menus lateraux, cartes,
listes d'evenements, fils de syndication. Ces pages presentent donc encore des
elements sans style.

### Sixieme tour : compatibilite completee, puis portage

**Phase 1 — compatibilite.** Les 52 classes `fr-*` sans regle sont couvertes.
Controle 8 ajoute : toute classe `fr-*` emise doit avoir une declaration. Il sert
aussi de compteur d'avancement du portage.

**Phase 2 — portage.** 581 occurrences portees, `fr-*` de 251 a 178.

| Passe | Porte | Occurrences |
|---|---|---|
| 1 | grille, espacement, typographie, utilitaires | 518 |
| 2 | etiquettes | 63 |

**Ce que le portage a exige du systeme**

| Version | Ajout |
|---|---|
| 0.10.0 | **Grille en 12 colonnes.** Le SDCD n'en avait pas : sa grille etait pilotee par `--sdcd-cols`, ce qui convient a un composant mais pas a une page. Le portage etait impossible sans elle. |
| 0.10.0 | Espacement au point de rupture `md`. |
| 0.10.1 | `.sdcd-tags`, conteneur d'etiquettes. |

**Decisions prises**

- *L'espacement est normalise sur l'echelle du systeme.* Onze valeurs se
  decalent — 48 px vers 40, 96 px vers 64. C'est le role d'une echelle. Une
  valeur non nulle ne tombe jamais a zero : normaliser un espacement est une
  chose, le supprimer en est une autre.
- *`fr-col` et `fr-col-sm` nus ne sont pas portes.* En flexbox DSFR ils
  signifient « part egale », ce qu'une grille a 12 colonnes n'exprime pas.
- *Le decalage de colonnes reste absolu.* Trois implementations d'un decalage
  relatif ont ete mesurees au navigateur ; aucune ne tient. Il ne convient donc
  qu'a une colonne qui ouvre sa ligne.

**Pourquoi le reste est un autre travail**

Les 178 classes restantes sont des composants, et **leurs structures different** :
le DSFR imbrique `fr-card__body > fr-card__content`, le SDCD a
`sdcd-card__corps` directement. Renommer les deux vers `__corps` produirait un
double rembourrage. Ces familles demandent une **reecriture du balisage**
gabarit par gabarit, avec verification visuelle — pas un renommage.

`fr-tag` et `fr-tags-group` etaient les seules dont la correspondance etait
reellement 1:1.

### Portage, suite : boutons, liens, alertes

`fr-*` de 178 a **169** (le compteur remonte de 164 a 169 parce que le controle
8 voit desormais les classes injectees, cf. plus bas).

| Porte | Occurrences |
|---|---|
| boutons, groupes, fermetures | 53 |
| liens et alertes | 27 |

**Portage sensible au contexte.** En DSFR, `.fr-btn` **seul est primaire** ; dans
le SDCD, `.sdcd-button` **seul est neutre**. Un renommage direct aurait rendu
invisibles les boutons sans modificateur. La variante est donc deduite des
autres jetons de l'attribut.

**Une premiere version du script a casse dix gabarits.** Sa deduplication
operait sur tous les jetons de l'attribut, fragments de syntaxe Django compris,
et supprimait les repetitions de `{%`, `if` et `endif`. **Le controle 4 l'a
signale avant tout commit et tout deploiement.** Le script ignore desormais tout
attribut contenant du code de gabarit — 97 dans le depot, laisses a une
relecture manuelle.

### Quatre defauts du systeme, encore

| Version | Defaut |
|---|---|
| 0.11.0 | Pas de **groupe de boutons** : chaque integration alignait ses actions a la main. |
| 0.11.0 | Pas de **tertiaire bordee**. Le DSFR distingue bordee et sans bordure a raison : bordee, l'action se lit comme un bouton ; sans bordure, comme un lien. |
| 0.11.1 | **`.sdcd-lien` ne fonctionnait que sur `<a>`.** Couleur et soulignement venaient de la regle `a` de `base.css` ; un bouton presente comme un lien n'heritait de rien. |
| 0.11.1 | Pas de variante compacte d'alerte. |

### La page de connexion s'affichait de travers

Constatee en la regardant, pas en la mesurant.

- **`.fr-password` etait declaree avec `.fr-search-bar`** en `flex` ligne. La
  barre de recherche est bien une ligne ; le bloc mot de passe est une colonne.
  Le champ et sa case « Afficher » se chevauchaient.
- **`.fr-label { display: block }`** s'appliquait aussi a l'intitule d'une case,
  qui passait donc a la ligne.
- **Deux classes sans regle** — `fr-password__input`, `fr-footer__content-desc`.

### Angle mort du controle 8, corrige

Ces deux classes sont injectees par le filtre `add_class` de
`django-widget-tweaks`, et n'apparaissent dans aucun attribut `class=` litteral.
Le controle ne lisait que ces attributs. Il lit desormais les deux sources :
**169 classes vues au lieu de 164**. Teste a l'envers.

### Portage des composants : 78 % du chemin

| | Classes | Occurrences |
|---|---|---|
| `sdcd-*` | **237** | **1 063** |
| `fr-*` | 122 | 283 |

Familles portees dans cette passe : **cartes** (84 occurrences, 11 gabarits),
**menu lateral** (28), **titres h5/h6, images fluides, bandeaux, tuiles, fils
d'Ariane, badges** (74).

### Sept lacunes de plus dans le systeme (0.12.0 et 0.13.0)

| | |
|---|---|
| Carte | Six modificateurs — `--horizontal`, `--gris`, `--sans-fond`, `--sans-bordure`, `--ombre`, `--telechargement` — plus `__actions` et `--cliquable` |
| Carte | `__media` porte `order: -1` : le composant React place le media en premier, un gabarit le place souvent en dernier. Les deux ordres rendent la meme chose |
| Typographie | `h5` et `h6` : l'echelle s'arretait a `h4`, le CMS emploie 27 titres de ces niveaux |
| Utilitaire | `.sdcd-image-fluide` — present dans dix-huit gabarits sans que le systeme le fournisse |
| Menu lateral | `--collant` |
| Bandeau, tuile, fil d'Ariane, badge | elements manquants : `__titre`, `__lien`, `__media`, `__meta`, `__liste`, `__bouton`, `.sdcd-badges`, `--sm` |

**Sans les modificateurs de carte, le portage aurait supprime une capacite
editoriale existante** — le rediger choisit fond, bordure et ombre pour chaque
carte. Une regression deguisee en migration.

### Deux decisions de fond

- **`fr-card__body > fr-card__content` se replie en un seul `__corps`.** La
  classe est gardee sur le div exterieur et retiree de l'interieur : la laisser
  aurait double le rembourrage.
- **`fr-sidemenu__item--active` est simplement retire.** Le gabarit pose deja
  `aria-current="page"` sur le lien, que le systeme stylise. Une classe qui
  double un etat ARIA finit toujours par diverger de lui.

### Ce qui reste — 283 occurrences

`fr-col` (20, exclu a dessein), `fr-link` et `fr-btn` (39, variantes d'icone et
reseaux sociaux sans equivalent), `fr-nav` (15), `fr-fieldset` (14), `fr-footer`
(13), `fr-collapse` (11), `fr-menu` et `fr-password` (16).

### Portage acheve — plus aucune classe DSFR

| | Avant | Apres |
|---|---|---|
| Classes `fr-*` emises | 251 | **0** |
| Classes `sdcd-*` | 99 | **plus de 260** |
| `compat-dsfr.css` | 2 682 regles, 134 Ko | **supprimee** |

Ne subsistent que des identifiants (`fr-sidemenu-wrapper-*`) et des attributs
`data-fr-*`, qui ne sont pas des classes : les renommer casserait des liens
`aria-controls` sans rien apporter.

### Ce que le portage a exige au-dela des gabarits

**Le code Python stockait des classes comme donnees.** Cent vingt valeurs —
type de bouton, taille de lien, icone, proportion d'image — proposees au rediger
dans l'administration puis ecrites en base. Les porter demandait deux gestes :
changer ce que le code propose, et **reecrire ce que la base contient deja**.
La migration `0081` s'en charge, avec une garde : une chaine n'est traduite que
si TOUS ses jetons sont des classes connues. Un texte redactionnel ou une URL
contenant « fr-btn » n'est pas touche — teste sur neuf cas dont quatre negatifs.

**L'echelle de marges ne coincide pas.** Le DSFR compte en `w` (1w = 8 px), le
SDCD a ses propres pas. Le rediger continue de choisir un nombre de `w` — changer
cette interface reformerait toutes les pages — mais la classe emise est ramenee
au pas du systeme le plus proche.

### Trois defauts fonctionnels, anterieurs au portage

Aucun n'etait cause par la migration ; tous ont ete mis au jour par elle.

- **La preference de theme rendue par le serveur etait ignoree.** Le gabarit
  posait `data-fr-scheme` sur `<html>` ; `sdcd.js` lit `data-theme`.
- **Le bouton « Reglages d'affichage » etait inerte.** Il portait
  `data-fr-opened` et pointait sur `fr-theme-modal`, deux crochets du JavaScript
  du DSFR parti avec lui.
- **Dix-huit classes de teinte n'existaient nulle part.** Le rediger choisissait
  une couleur pour un exergue, un badge ou une citation, et rien ne se
  produisait. Le defaut vivait dans le CMS depuis l'origine.

Les teintes sont desormais implementees **en accent seulement** — filet,
bordure, jamais le texte. Ce n'est pas une preference : `--sdcd-chart-1` ne fait
que 3,0:1 sur blanc et echouerait le contrat de contraste comme couleur de
texte. Une bordure releve de WCAG 1.4.11 et n'a besoin que de 3:1.

### Le controle 8 change de nature

Il ne mesure plus une couverture — il **interdit** l'emission d'une classe DSFR.
Teste a l'envers.

---

## À venir

Les entrées suivantes seront ajoutées au fil du portage :

- portage progressif des gabarits vers `sdcd-*`, ce qui allégera d'autant
  `compat-dsfr.css` puis permettra de retirer l'alias `dsfr/` ;
- remplacement des classes d'icônes `fr-icon-*` par `ri-*` ;
- substitution de la marque d'État française par la marque congolaise ;
- production des fichiers d'icône référencés par `sdcd_favicon`.

---

## 2026-09-02 — Site vitrine complet, page de connexion, tableau de bord

Le site de démonstration montre désormais tout ce que le CMS sait faire, à la
manière de sites.beta.gouv.fr : rubrique « Exemples » (page d'atterrissage,
site vitrine, blog, agenda, catalogue, formulaire), documentation, en-tête
complet (recherche, connexion, bandeau), lettre d'information, réseaux sociaux,
mega-menu. Contenu rédigé en contexte congolais.

| Fichier | Modification |
|---|---|
| `sites_conformes/core/vitrine/` | Ajouté — contenu du site vitrine (accueil, exemples, documentation, configuration, images, fabriques de blocs) |
| `sites_conformes/core/showcase_images/` | Ajouté — 20 compositions plates aux couleurs du SDCD, sans texte ni photo tierce |
| `sites_conformes/core/management/commands/create_showcase_pages.py` | Réécrit — construit la rubrique Exemples, les entrées de blog, d'agenda et de catalogue, le formulaire, les réglages et les menus ; idempotent |
| `sites_conformes/core/tests/test_showcase_pages.py` | Réécrit — chaque page validée bloc par bloc (comme le formulaire d'édition), rendu, en-tête, menus, connexion sur le domaine d'administration |
| `sites_conformes/core/blocks/cards.py` | `image_ratio` : valeur par défaut « h3 » (hors choix) → vide ; `enlarge_link` tolère les sous-blocs absents |
| `sites_conformes/core/migrations/0086_*`, `blog/0065_*`, `events/0037_*` | Migrations de schéma correspondantes |
| `sites_conformes/dashboard/views.py`, `templates/wagtailadmin/home/panels/_tutorials.html` | Panneau « Tutoriels » (appel réseau vers sites.beta.gouv.fr, vignettes Sites Faciles) remplacé par des guides locaux |
| `sites_conformes/dashboard/templates/wagtailadmin/login.html`, `templates/sites_conformes_core/standalone.html` | Page de connexion : en-tête et pied réduits (les liens du site public répondaient 404 sur le domaine d'administration) |
| `config/settings.py` | `LOGIN_URL`/`LOGOUT_URL` absolus vers `WAGTAILADMIN_BASE_URL` quand l'instance ne sert pas le back-office |
| `sdcd/templates/sdcd/breadcrumb.html` | Même structure que l'include des pages (bouton et repli sur mobile) |
| `sdcd/static/sdcd/` | SDCD 0.18.0 |

---

## 2026-09-02 — Wagtail 8.0, menus déroulants, en-tête mobile

| Fichier | Modification |
|---|---|
| `pyproject.toml`, `uv.lock` | Wagtail 7.4.2 → 8.0 ; wagtailmenus 4.1 ; wagtail-localize 1.14.5. Aucune migration, aucun code à adapter (vérificateur sans défaut, 294 tests OK sur image reconstruite) |
| `sites_conformes/menus/templates/sites_conformes_menus/blocks/link.html` | Accès rapides de l'en-tête en liens tertiaires (étaient des boutons primaires) |
| `…/main_menu_megamenu.html`, `…/main_menu_submenu.html` | `type="menu"` (inexistant) → `type="button"` ; pilotés par sdcd.js |
| `sites_conformes/templates/sites_conformes_core/blocks/header.html` | Sous 900 px, accès rapides, connexion et recherche passent dans le panneau du menu (la rangée débordait de 900 px) |
| `sites_conformes/templates/sites_conformes_core/blocks/notice.html` | Bouton « Masquer le message » en bouton tertiaire avec icône |
| `sites_conformes/static/css/style.css` | En-tête large : plus de marge négative (recouvrait le bandeau) ; boutons secondaires lisibles sur image assombrie quel que soit le thème ; cases à cocher des formulaires à 20 px |
| `config/settings.py`, `.env.example` | `SF_ADMIN_URL` pour le bouton de connexion (poser `WAGTAILADMIN_BASE_URL` sur l'instance publique faisait charger les images depuis le domaine d'administration) |
| `sites_conformes/core/vitrine/` | Résumés (`search_description`) des pages d'exemple ; tuiles sans image ; exemples de composants lus depuis l'index des modèles |
| `sdcd/static/sdcd/` | SDCD 0.18.0 (menus déroulants, média de carte borné, cibles tactiles) |

---

## 2026-09-02 — Affinage du rendu, Wagtail 8, index Documentation

Relecture page par page sous Brave (bureau 1280 px et mobile 375 px), puis
corrections ; mise a jour de Wagtail 7.4 vers 8.0 (aucune migration ni
adaptation de code necessaires, 294 tests) ; theme SDCD pour l'admin Django
livre dans le depot SDCD (`adaptateurs/django-admin`).

| Fichier | Modification |
|---|---|
| `sites_conformes/core/vitrine/` | Accueil : pictogrammes, bandes de fond ; articles, evenements, fiches : bandeau d'en-tete ; index « Documentation » et guides deplaces dessous ; resumes ; images de contenu recadrees, remplacees a l'import quand le fichier change (rendus purges) |
| `sites_conformes/core/abstract.py` | `cover()` se replie sur `header_image` (listes et entrees recentes illustrees) |
| `sites_conformes/templates/.../blocks/share.html`, `follow.html` | Boutons de partage et de reseaux sociaux discrets, en ligne |
| `sites_conformes/core/templates/.../blocks/tabs.html`, `accordions.html` | Panneaux caches sauf le premier ; accordeons alignes a gauche |
| `sites_conformes/static/css/style.css` | Cases a cocher 20 px, portrait de la fiche contact en medaillon |
| `sdcd/static/sdcd/` | SDCD 0.18.1 |
| `pyproject.toml`, `uv.lock` | Wagtail 8.0, wagtailmenus 4.1, wagtail-localize 1.14.5 |
| `config/settings.py` | `SF_ADMIN_URL` pour le bouton de connexion de l'instance publique |

---

## 2026-09-03 — Fusion de l'amont v4.2.0-rc1

Reprise des 15 commits de l'amont depuis la base du fork : authentification a
deux facteurs (wagtail-2fa), libelle et filtres du bouton « voir tout » des
blocs d'entrees recentes, correction des filtres de catalogue, classes de
formulaires, crochets de personnalisation de la recherche, outillage (bandit,
deptry), documentation Sphinx. Conserve cote RDC : Wagtail 8, gabarits et
classes SDCD, politique CSP/HSTS, README.

| Fichier | Modification |
|---|---|
| `pyproject.toml`, `uv.lock` | `wagtail>=8.0` conserve (l'amont reste en 7.x) ; `wagtail-2fa==1.8.0` ajoute |
| `sites_conformes/dashboard/compat.py`, `config/settings.py` | Cale `wagtail.users.widgets` (retire dans Wagtail 8, encore importe par wagtail-2fa — issue labd/wagtail-2fa#283), resolue paresseusement |
| `sites_conformes/*/migrations/00xx_merge_*`, `..._alter_*_body_*` | Migrations de raccord entre les branches (definitions de blocs) |
| `sites_conformes/core/templates/.../blog_recent_entries.html`, `events_recent_entries.html` | Bouton « voir tout » configurable et filtre, en classes SDCD |
| `sites_conformes/forms/templates/.../form_page.html` | `DSFR_MARK_OPTIONAL_FIELDS` repris ; champs rendus par `dsfr_form_field` (SDCD) |
| `sites_conformes/*/tests/test_*.py` | Tests amont portes vers les classes SDCD |
| `sites_conformes/templates/.../blocks/share.html` | Classes de plateforme retirees (plus de regle) |
| `config/settings.py` | `TIME_ZONE` par defaut `Africa/Kinshasa` (surchargeable par la variable `TIME_ZONE`) ; `WAGTAIL_USER_TIME_ZONES` limite aux noms canoniques « Region/Ville » + UTC : l'alias `localtime` de tzdata faisait echouer `Intl.DateTimeFormat` et donc la traduction de la liste des fuseaux dans le compte utilisateur |

---

## 2026-09-03 — Mega-menu, etapier, pages publiques des composants

| Fichier | Modification |
|---|---|
| `sites_conformes/menus/templates/.../main_menu_megamenu.html`, `..._column.html`, `core/templates/.../menus/mega_menu.html`, `mega_menu_category.html` | Mega-menu recompose : en-tete a gauche (titre en paragraphe, description visible, lien vers la rubrique), « Fermer » a droite ; colonnes a intitule non cliquable (plus de lien vers « # ») et liste propre au mega-menu (`sdcd-megamenu__liste`) ; conteneur aligne sur l'en-tete. Regles dans SDCD 0.18.2 |
| `sites_conformes/core/templates/.../blocks/stepper.html`, `core/blocks/basics.py` | Etapier : compte d'etapes au-dessus du titre, jauge, « Etape suivante », puis frise verticale des etapes avec leur etat (faite, courante, a venir), dit aussi en toutes lettres pour les lecteurs d'ecran |
| `sites_conformes/core/management/commands/create_showcase_pages.py`, `core/vitrine/exemples.py`, `configuration.py` | Les modeles de pages a copier vivent hors du site (sans URL) : le menu les reliait par `href="None"`. Un index public « Composants » sous Exemples recoit une copie de chaque modele ; le menu relie les copies. Resumes des dix modeles |
| `sites_conformes/core/tests/test_showcase_pages.py` | Composants publics sous `/exemples/composants/`, aucun `href="None"` ni `href="#"` dans l'en-tete, etats de l'etapier rendus |
| `sites_conformes/locale/fr/LC_MESSAGES/django.po`, `django.mo` | « Next step: », « completed », « current step » |
| `sdcd/static/sdcd/components.css` | SDCD 0.18.6 (mega-menu, etapier, menu lateral, navigation mobile, tuiles, cartes) |
| `sites_conformes/menus/templatetags/wagtail_dsfr_menus_tags.py`, `templates/.../header.html`, `menus/templates/.../main_menu_megamenu.html`, `main_menu_submenu.html` | Le menu est rendu deux fois (bureau, mobile) avec les memes identifiants de region : le JavaScript n'ouvrait que la premiere, et ni mega-menu ni sous-menu ne s'ouvraient dans le panneau mobile. La navigation mobile passe un suffixe `-mobile` aux identifiants |
| `sites_conformes/core/templates/.../blocks/pagetree.html` | La racine de l'arbre du menu lateral etait toujours marquee page courante ; puces et retrait des listes retires dans SDCD 0.18.3 |
| `sites_conformes/core/management/commands/create_showcase_pages.py` | Les copies de composants recoivent chacune une vignette de la vitrine (les modeles amont portaient des illustrations de leur site d'origine) ; leur arbre de pages est rattache a l'index Composants, celui des modeles a leur index (l'identifiant amont n'existait pas et la page ne validait plus) |
| `sites_conformes/core/vitrine/composants.py` (nouveau), `outils.py`, `exemples.py`, `create_showcase_pages.py` | Les dix pages de composants sont redigees (tuiles, cartes, accordeons, etapiers, en-tetes et bandeaux, blocs simples, mise en valeur, grilles, menu lateral, onglets et fiches contact) avec un contenu en contexte congolais et les images de la vitrine ; elles remplacent les copies des modeles amont. Fabriques ajoutees : carte horizontale, image centree, lien simple, separateur, ancre, texte et appel a action, fond avec menu lateral ; couleur de badge « nouveau » (hors choix) remplacee par « info ». La commande ne cherche les pages de composants que sous leur index : elles partagent leurs slugs avec les modeles hors site |
| `sites_conformes/core/templates/.../blocks/image_and_text.html`, `core/blocks/basics.py` | La colonne de texte prenait une classe inexistante (« 12-8 ») et passait sous l'image : largeur calculee dans le bloc |
| `.../blocks/full_width_background.html` | Image de fond en couverture sous un voile sombre, texte blanc (`sdcd-fond-image`) ; elle s'affichait a sa taille, coupee, sous un texte sombre |
| `.../heros/hero_image_text.html` | Image d'en-tete en 4:3 (720x540) au lieu du carre 600x600 |
| `.../blocks/tabs.html` | Icone « case cochee » retiree des onglets (reliquat du modele amont) |
| `sites_conformes/core/showcase_images/picto-*.png`, `illustration-*.png`, `portrait-*.png` | Pictogrammes sur fond transparent ; illustrations et portraits regeneres avec leur glyphe (les fichiers etaient vides) |
| `sites_conformes/core/vitrine/accueil.py` | Les quatre tuiles « bonnes raisons » en horizontal, pictogramme a droite |
| `sdcd/static/sdcd/` | SDCD 0.18.6 |
| `.../blocks/multicolumns.html` | Rembourrage vertical seulement quand le bloc a un fond ; image de fond en couverture sous voile |
| `sites_conformes/static/css/style.css` | Deux listes de boutons successives espacees |
| `sites_conformes/core/vitrine/images.py` | Cache vide apres remplacement d'une image (Wagtail gardait les anciens noms de rendus) ; l'instance publique reste a redemarrer |
| `sites_conformes/core/vitrine/exemples.py`, `create_showcase_pages.py` | Index des exemples : les rubriques (actualites, agenda, catalogue, formulaire, composants) en cartes ; guides de la documentation illustres ; page de contact reecrite ; la carte « Modeles » de l'accueil renvoie vers les composants |
| `sites_conformes/forms/templates/.../form_page.html` | Introduction du formulaire bornee a la mesure de lecture |
| `sites_conformes/static/css/style.css` | Boutons d'en-tete : `align-items: left/right` (valeurs invalides) remplaces par `flex-start/flex-end` — sur mobile, les boutons d'un en-tete aligne a gauche etaient centres |
| `sdcd/static/sdcd/` | SDCD 0.18.8 (listes de boutons en colonne, carte horizontale empilee sur mobile, menu lateral replie avec chevron) |
| `.../blocks/full_width_background_with_sidemenu.html` | Sur mobile, le menu lateral demarre replie derriere son bouton « Dans cette rubrique » (le bouton etait `hidden`, la liste prenait tout l'ecran avant le contenu) ; espace apres une liste de boutons |
| `.../heros/hero_image_text.html`, `static/css/style.css` | Sous 900 px, l'image de l'en-tete ne touche plus les boutons |
