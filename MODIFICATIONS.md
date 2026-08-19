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

## À venir

Les entrées suivantes seront ajoutées au fil du portage :

- retrait de `django-dsfr` et de ses gabarits ;
- ajout de `django-sdcd` ;
- substitution de la marque d'État française par la marque congolaise ;
- remappage des 233 classes CSS `fr-*` vers `sdcd-*`.
