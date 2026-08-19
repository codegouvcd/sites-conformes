# Sites conformes RDC

Gestionnaire de contenu permettant de créer des sites `.gouv.cd` conformes,
habillés par le **Système de design RDC (SDCD)**.

> **Statut : DSFR retiré, habillage SDCD en place.** `django-dsfr` est
> désinstallé ; l'application `sdcd/` le remplace, et l'alias `dsfr/` permet aux
> gabarits hérités de fonctionner sans modification. La contrainte juridique est
> levée. Reste à porter les gabarits en `sdcd-*` et à produire la marque d'État
> congolaise ; le CMS n'a pas encore été exécuté contre une base de données.

Le README d'origine est conservé sous [`README.amont.md`](README.amont.md).

## Origine et licence

Ce dépôt est un fork de
**[numerique-gouv/sites-conformes](https://github.com/numerique-gouv/sites-conformes)**
(anciennement « Sites Faciles »), développé par la DINUM pour l'État français.

Base du fork : **v4.1.0**, commit `1d36360` du 18 août 2026.

### AGPL-3.0 — ce que cela nous engage à faire

L'amont est sous **GNU Affero General Public License v3.0**, conservée à
l'identique dans [`LICENSE`](LICENSE). Trois obligations en découlent, actées :

1. **Publication du code source.** L'AGPL couvre l'usage en réseau : tout site
   servi au public à partir de ce code doit en publier les sources
   correspondantes, nos modifications comprises. Une simple mise en ligne
   déclenche l'obligation, sans qu'aucun binaire soit distribué.
2. **Signalement des modifications.** Les versions modifiées doivent porter
   mention du changement et de sa date — voir [`MODIFICATIONS.md`](MODIFICATIONS.md).
3. **Maintien de la licence.** Tout dérivé reste sous AGPL-3.0. Nous ne pouvons
   pas relicencier, y compris dans le cadre d'un marché public.

### ⚠️ Contrainte juridique : le DSFR ne nous est pas accessible

Le README amont énonce, au sujet du Système de design de l'État français :

> « Il est formellement interdit à tout autre acteur d'utiliser le Système de
> Design de l'État (les administrations territoriales ou tout autre acteur
> privé) pour des sites web ou des applications. »

La République Démocratique du Congo est un « autre acteur » au sens de cette
clause. **Retirer le DSFR n'est donc pas une option de personnalisation, c'est
une condition de légalité.** C'est précisément la raison d'être du SDCD.

Cette contrainte ne porte que sur le design. Le code applicatif, sous AGPL,
reste librement réutilisable.

## Ce qu'il faut remplacer — état des lieux mesuré

Relevé sur la base du fork, à des fins de chiffrage :

| Couplage au DSFR | Mesure |
|---|---|
| Fichiers mentionnant `dsfr` | 204 |
| Templates HTML concernés | 61 sur 125 |
| Fichiers Python concernés | 139 sur 381 |
| Occurrences `DSFR` en Python **hors migrations** | 34, dans 10 fichiers |
| Classes CSS `fr-*` distinctes dans les templates | **233** (1 331 occurrences) |

Le couplage Python est superficiel : `from dsfr.constants`, `from dsfr.forms`,
et les tags `{% dsfr_pagination %}`, `{% dsfr_form_field %}`,
`{% dsfr_breadcrumb %}`. Le gros des occurrences est du bruit de migration
Wagtail (renommages du modèle `dsfrconfig`).

L'essentiel du travail porte donc sur les 233 classes CSS :

| Nature | Nombre | Couverture SDCD |
|---|---|---|
| Composants | 153 (65 %) | couverts — les 17 plus fréquents ont leur équivalent |
| Grille et conteneur | 36 (15 %) | couverts, API différente (`fr-col-12` → `--sdcd-cols`) |
| Utilitaires d'espacement | 34 (14 %) | couverts depuis SDCD 0.5.0 |
| Utilitaires typographiques | 10 (4 %) | couverts depuis SDCD 0.5.0 |

## Ce que `sdcd` fournit

`django-dsfr` exposait 43 entrées. `sdcd` en fournit **40 tags** plus les
auxiliaires : parité entière, pour qu'aucun gabarit — présent ou futur — ne
tombe sur un tag manquant.

Le CMS n'en emploie lui-même que **14**, plus quatre gabarits qu'il étend par
chemin (`dsfr/header.html`, `dsfr/footer.html`, `dsfr/follow.html`,
`dsfr/form_snippet.html`). Ces quatre-là définissent les mêmes blocs que
l'amont : le CMS les surcharge sans modification.

**Python** — trois modules, tous aliasés :

| Import | Éléments |
|---|---|
| `dsfr.constants` | `COLOR_CHOICES`, `COLOR_CHOICES_ILLUSTRATION`, `COLOR_CHOICES_SYSTEM`, `IMAGE_RATIOS`, `VIDEO_RATIOS`, `NOTICE_TYPE_CHOICES`, `DJANGO_DSFR_LANGUAGES` |
| `dsfr.forms` | `DsfrBaseForm`, `DsfrBoundField`, `DsfrDjangoTemplates` |
| `dsfr.utils` | `dsfr_input_class_attr`, `parse_tag_args`, `lazy_static` |

Les 8 tags locaux de `sites_conformes/core/templatetags/wagtail_dsfr_tags.py`
(`settings_value`, `root_url`, `canonical_url`, `language_selector`,
`richtext_p_add_class`, `toggle_url_filter`, `event_date_range`,
`table_has_heading_row`) **ne dépendent pas du DSFR** : ils sont inchangés.

## Vérifier

```bash
.venv/Scripts/python.exe verifier_sdcd.py
```

Quatre contrôles : rendu des tags `sdcd_*`, rendu des tags `dsfr_*` via l'alias,
existence de toute classe `sdcd-*` émise, compilation des 55 gabarits du CMS.

## Plan de portage

1. ~~**`django-sdcd`**~~ — **fait.** 40 tags, parité entière avec l'amont.
2. ~~**Retrait de `django-dsfr`**~~ — **fait.** Désinstallé, retiré de
   `pyproject.toml` et de `uv.lock`. L'alias `dsfr/` prend le relais.
3. **Portage des gabarits** — remplacer `fr-*` par `sdcd-*` dans les 61
   fichiers, ce qui allégera `compat-dsfr.css` puis permettra de retirer
   l'alias. Non commencé.
4. **Marque d'État** — armoiries, filet tricolore et bloc « République
   Démocratique du Congo » à la place de la Marianne et du bloc-marque français.
5. **Multilinguisme** — six langues, dont quatre langues nationales. Wagtail
   Localize est déjà présent dans l'amont. Attention : la fonte doit couvrir
   `ɛ`, `ɔ` et `ŋ` — le SDCD fournit `outils/verifier-fontes.html` pour le
   contrôler.

## Pile technique

Reprise de l'amont sans changement : **Django 6**, **Wagtail 7.2**,
**PostgreSQL 14-17**, **Python 3.12–3.14**. Dépendances par `uv`, tâches par
`just`, conteneurs par `docker compose`.

## Suivi de l'amont

Le dépôt distant `upstream` pointe sur le dépôt français ; le push y est
volontairement désactivé.

```bash
git fetch upstream && git log --oneline HEAD..upstream/main
```

Le travail se fait sur la branche `sdcd`. Garder les modifications regroupées et
documentées facilite la reprise des évolutions amont — l'AGPL nous permet d'en
bénéficier indéfiniment, à condition de rester synchronisés.

## Documentation liée

| Document | Contenu |
|---|---|
| [`MODIFICATIONS.md`](MODIFICATIONS.md) | Journal des écarts avec l'amont (obligation AGPL) |
| [`README.amont.md`](README.amont.md) | README d'origine, conservé pour attribution |
| `../SDRDC/readme.md` | Système de design RDC — doctrine, jetons, composants |
| `../SDRDC/CHANGELOG.md` | Journal du système de design |
