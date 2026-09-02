"""Images du site vitrine.

Des compositions plates aux couleurs du systeme de design, sans texte ni
photographie tierce : elles se recadrent sur mobile et n'engagent aucun droit.
Elles sont versionnees dans `showcase_images/` et importees dans une collection
dediee ; l'import est idempotent (par titre).
"""

import os

from wagtail.images import get_image_model

from sites_conformes.core.services.accessors import get_or_create_collection
from sites_conformes.core.utils import import_image, overwrite_image

COLLECTION = "Site vitrine"
DOSSIER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "showcase_images")

# nom de fichier → titre lisible dans la mediatheque
TITRES = {
    "hero-accueil": "Vitrine — en-tête de l’accueil",
    "hero-atterrissage": "Vitrine — en-tête de la page d’atterrissage",
    "hero-vitrine": "Vitrine — bandeau du site vitrine",
    "actualite-numerique": "Vitrine — actualité numérique",
    "actualite-accessibilite": "Vitrine — actualité accessibilité",
    "actualite-formation": "Vitrine — actualité formation",
    "actualite-tribune": "Vitrine — tribune",
    "evenement-atelier": "Vitrine — atelier",
    "evenement-conference": "Vitrine — conférence",
    "evenement-concertation": "Vitrine — concertation",
    "evenement-formation": "Vitrine — formation",
    "service-etat-civil": "Vitrine — service état civil",
    "service-passeport": "Vitrine — service passeport",
    "service-entreprise": "Vitrine — service entreprises",
    "service-impots": "Vitrine — service impôts",
    "portrait-agente": "Vitrine — portrait d’une agente",
    "portrait-agent": "Vitrine — portrait d’un agent",
    "illustration-blocs": "Vitrine — illustration des blocs",
    "illustration-redaction": "Vitrine — illustration de la rédaction",
    "illustration-securite": "Vitrine — illustration de la sécurité",
    "picto-conformite": "Vitrine — pictogramme conformité",
    "picto-autonomie": "Vitrine — pictogramme autonomie",
    "picto-budget": "Vitrine — pictogramme budget",
    "picto-securite": "Vitrine — pictogramme sécurité",
}


def importer_images(ecrire=print):
    """Importe les images absentes et renvoie {nom: Image}."""
    Image = get_image_model()
    collection = get_or_create_collection(COLLECTION)
    images = {}
    importees = 0
    remplacees = 0
    for nom, titre in TITRES.items():
        chemin = os.path.join(DOSSIER, f"{nom}.png")
        image = Image.objects.filter(title=titre).first()
        if image is None:
            if not os.path.isfile(chemin):
                ecrire(f"  image absente : {chemin}")
                continue
            image = import_image(full_file_path=chemin, title=titre)
            image.collection = collection
            image.save()
            importees += 1
        elif os.path.isfile(chemin) and image.file.size != os.path.getsize(chemin):
            # Le fichier a change depuis l'import (image redessinee) : on le
            # remplace, sinon la base garderait l'ancienne version a jamais.
            image = overwrite_image(image=image, full_file_path=chemin, title=titre)
            # Les rendus en cache sont ceux de l'ancien fichier : sans cette
            # purge, les pages continuaient d'afficher l'image d'avant.
            image.renditions.all().delete()
            remplacees += 1
        images[nom] = image
    ecrire(f"  images : {len(images)} disponibles, {importees} importées, {remplacees} remplacées")
    return images
