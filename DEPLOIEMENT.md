# Déploiement sur Dokploy

Cible : **bgvps3.beinng.tech** — instance Dokploy vérifiée accessible et saine
(`/api/health` → `{"ok":true}`).

> **Ce document décrit une procédure non exécutée.** Le déploiement demande un
> accès à Dokploy — clé d'API ou session dans l'interface — dont je ne dispose
> pas. Tout ce qui pouvait être vérifié en amont l'a été (voir « Vérifié avant
> déploiement »).

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
