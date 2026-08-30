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

---

## À venir

Les entrées suivantes seront ajoutées au fil du portage :

- portage progressif des gabarits vers `sdcd-*`, ce qui allégera d'autant
  `compat-dsfr.css` puis permettra de retirer l'alias `dsfr/` ;
- remplacement des classes d'icônes `fr-icon-*` par `ri-*` ;
- substitution de la marque d'État française par la marque congolaise ;
- production des fichiers d'icône référencés par `sdcd_favicon`.
