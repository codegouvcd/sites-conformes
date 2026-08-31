#!/bin/sh -l
set -ex

export USE_UV=0
export USE_DOCKER=0 # Commands run from inside docker shouldn't be prefixed

# Le justfile declare `set dotenv-load` : `just` lit /app/.env avant toute
# recette. Or certaines plateformes de deploiement ecrivent ce fichier a partir
# des variables de l'application SANS quoter les valeurs. Il suffit alors qu'une
# seule contienne une espace — SITE_NAME=Sites conformes RDC, par exemple — pour
# que `just` s'arrete sur « Error parsing line », et le conteneur boucle sans
# jamais demarrer. Quoter cote plateforme ne suffit pas : elle reecrit le fichier
# a chaque deploiement, guillemets retires.
#
# Les variables sont de toute facon deja presentes dans l'environnement du
# conteneur. On quote plutot que de supprimer le fichier, pour ne rien perdre
# s'il portait une valeur absente de l'environnement.
if [ -f /app/.env ]; then
    awk '
        /^[A-Za-z_][A-Za-z0-9_]*=/ {
            cle = substr($0, 1, index($0, "=") - 1)
            valeur = substr($0, index($0, "=") + 1)
            premier = substr(valeur, 1, 1)
            if (valeur ~ / / && premier != "\"" && premier != "\047") {
                print cle "=\"" valeur "\""
                next
            }
        }
        { print }
    ' /app/.env > /app/.env.quote && mv /app/.env.quote /app/.env
fi

just deploy

if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:$CONTAINER_PORT
else
    gunicorn config.wsgi:application --bind 0.0.0.0:$CONTAINER_PORT
fi

exec "$@"
