# Déploiement sur Dokploy

**Déploiement effectué et vérifié.** Site en ligne :
<https://sdcd-72-60-188-156.sslip.io>

| Élément | Valeur |
|---|---|
| Serveur | `bgvps3.beinng.tech` / `72.60.188.156` (`srv1032376`) |
| Dokploy | v0.30.2, port 3000 |
| Projet | **CODE.GOUV.CD**, environnement `production` |
| Application | `sdcd-cms` |
| Base | PostgreSQL 16, service `sdcd-db`, hôte interne `sdcd-db-ckpbyy` |
| Source | `git@github.com:codegouvcd/sites-conformes.git`, branche `sdcd` |
| Accès dépôt | Clé de déploiement **lecture seule** |
| Construction | `Dockerfile` |
| Domaine | `sdcd-72-60-188-156.sslip.io`, Let's Encrypt |
| Volume médias | Volume nommé **`sdcd-medias`**, uid 1000 |
| Administration | `/cms-admin/` (et non `/admin/`) |

## Secrets

Aucun secret ne figure dans ce dépôt ni dans les échanges. Sur le serveur :

| Fichier | Contenu |
|---|---|
| `/root/.dokploy-token` | Jeton d'API Dokploy |
| `/root/.sdcd-dbpass` | Mot de passe PostgreSQL, 32 caractères |
| `/root/.sdcd-admin-pass` | Mot de passe du compte `admin` Wagtail, 24 caractères |
| `/root/.ssh/dokploy_sdcd_deploy` | Clé privée de déploiement |

La `SECRET_KEY` Django, 60 caractères, est dans les variables d'environnement de
l'application, générée sur le serveur.

## Ce que le premier déploiement a coûté

**Cinq cycles**, cinq causes distinctes, toutes invisibles hors d'une exécution
réelle en configuration de production :

1. Chevron DSFR dans un `url()` — `collectstatic` échouait, conteneur en boucle
2. Quatre références DSFR dans le code Python — dont deux qui auraient renvoyé
   **500 sur l'administration**, sans empêcher le démarrage
3. Volume `/app/medias` appartenant à `root`, conteneur en uid 1000 — et volume
   **anonyme**, donc médias perdus à chaque redéploiement
4. Pictogrammes absents non tolérés par l'import des gabarits
5. Cinq références `{% static %}` mortes — dont le favicon, inclus par le gabarit
   de base, qui renvoyait **500 sur tout le site**

Les points 1, 2 et 5 relèvent du même mécanisme : `ManifestStaticFilesStorage`
échoue durement sur un fichier absent, à la collecte comme au rendu. Deux contrôles
ont été ajoutés à `verifier_sdcd.py` pour couvrir cette classe entière, **tous deux
testés à l'envers**.

## Reste à faire

- ~~Le dépôt est privé.~~ **Réglé le 2026-08-30.** Le dépôt est public et le pied
  de page offre le lien vers les sources, comme l'exige l'article 13 de l'AGPL —
  publier le dépôt ne suffisait pas, le lien devait être atteignable depuis le
  site. Vérifié avant bascule : `.env` jamais commité, aucune chaîne à forte
  entropie dans l'historique, et la seule `SECRET_KEY` en dur porte le préfixe
  `django-insecure-` de Django, dans `demo/` qui est exclu de l'image.
- **Aucune politique de sécurité de contenu.** `request.csp_nonce` est référencé,
  `django-csp` n'est pas installé.
- **Dokploy est servi en HTTP nu** sur le port 3000 : session d'administration et
  jeton d'API circulent en clair.
- Le sélecteur d'icônes de l'administration est réduit à un champ texte.
- Les 61 gabarits du CMS emploient encore les classes `fr-*` via `compat-dsfr.css`.

---

## Annexe — procédure d'origine

## Prérequis à régler avant de commencer

### 1. Accès du dépôt privé

`codegouvcd/sites-conformes` est **privé**. Dokploy doit pouvoir le cloner :

- soit installer l'**application GitHub Dokploy** sur l'organisation `codegouvcd`
  (Dokploy → *Settings* → *Git* → *GitHub*) ;
- soit déclarer une **clé de déploiement** : Dokploy → *Git* → *SSH Keys*, puis
  coller la clé publique dans GitHub → *Settings* → *Deploy keys* du dépôt.

Alternative : passer les deux dépôts en public. **L'AGPL-3.0 l'exigera de toute
façon** dès que le site sera servi au public — voir plus bas.

### 2. Base de données

Le CMS **exige PostgreSQL** : une de ses migrations emploie du SQL spécifique,
vérifié — `migrate` échoue sur SQLite. Créer dans Dokploy un service
**PostgreSQL 14 à 17**, dans le même projet, et relever l'URL interne qu'il
expose.

## Configuration de l'application

| Réglage | Valeur |
|---|---|
| Type | Application |
| Source | GitHub — `codegouvcd/sites-conformes` |
| Branche | `sdcd` |
| Type de build | **Dockerfile** (présent à la racine) |
| Port exposé | `8000` |
| Volume persistant | `/app/medias` |

Le `Dockerfile` installe les dépendances avec `uv sync --locked` puis exécute
`collectstatic` à la construction. L'`entrypoint.sh` lance `just deploy`
(migrations, pages de démarrage, index de recherche) puis `gunicorn`.

## Variables d'environnement

Minimum indispensable :

```
DATABASE_URL=postgres://UTILISATEUR:MOTDEPASSE@HOTE_INTERNE:5432/BASE
SECRET_KEY=<chaîne aléatoire de 50 caractères, à générer>
DEBUG=False
ALLOWED_HOSTS=sites.gouv.cd,bgvps3.beinng.tech
CSRF_TRUSTED_ORIGINS=https://sites.gouv.cd,https://bgvps3.beinng.tech
HOST_PROTO=https
HOST_URL=sites.gouv.cd
HOST_PORT=8000
CONTAINER_PORT=8000
SITE_NAME=Sites conformes RDC
MEDIA_ROOT=/app/medias
SF_USE_WHITENOISE=True
SF_PROD_SERVE_STATIC=True
WAGTAILADMIN_BASE_URL=https://sites.gouv.cd
```

**`SECRET_KEY` doit être générée, jamais reprise d'un exemple.** Depuis un
conteneur Python :

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

À renseigner directement dans l'interface Dokploy (section *Environment*), pas
dans un fichier versionné : `.env` est volontairement dans `.gitignore`.

Facultatif : `DEFAULT_FROM_EMAIL` et les `EMAIL_*` pour l'envoi de courriels,
`SENTRY_DSN` pour la supervision, les `S3_*` pour un stockage objet.

## Après le premier déploiement

```bash
# Depuis un terminal Dokploy sur le conteneur
python manage.py createsuperuser
```

L'administration Wagtail est ensuite accessible sur `/admin`.

## Obligation AGPL — à traiter avec le déploiement

L'AGPL-3.0 impose de publier les sources correspondantes de **tout service
accessible en réseau**. Dès que ce déploiement est ouvert au public :

1. passer `codegouvcd/sites-conformes` en **public** ;
2. rendre le lien vers les sources visible depuis le site — le pied de page
   convient.

Tant que le déploiement reste privé ou d'accès restreint, l'obligation ne se
déclenche pas.

## Vérifié avant déploiement

Ce qui a été contrôlé en local, et qui vaut pour la construction de l'image :

| Contrôle | Résultat |
|---|---|
| `manage.py check` | 0 erreur |
| `collectstatic` | 252 fichiers, dont les **14 fichiers SDCD** |
| Fichiers DSFR restants après collecte | **aucun** |
| `verifier_sdcd.py` | aucun défaut sur ses 4 contrôles |
| Gabarits du CMS compilés | 55/55 |
| Rendu des gabarits réels | 5/5, marque congolaise, 0 échec de contraste |
| `uv sync --locked` | réussi, `django-dsfr` absent du verrou |

## Ce qui n'a pas pu être vérifié

- **La construction de l'image Docker elle-même** : le démon Docker ne répond
  pas sur le poste de développement.
- **Aucune page servie par un vrai serveur HTTP Django** : les gabarits ont été
  rendus, les vues et les URL ne sont pas exercées.
- **Les migrations sur PostgreSQL** : seules celles compatibles SQLite ont été
  jouées. `migrate` complet reste à faire au premier déploiement — c'est
  précisément ce que fait `entrypoint.sh`.
