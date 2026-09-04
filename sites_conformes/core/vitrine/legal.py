"""Mentions légales et déclaration d'accessibilité du site de démonstration.

Les pages de départ ne contenaient qu'un « Entrez ici… » : un site vitrine qui
prêche la conformité ne peut pas garder ses pages légales vides. Le contenu
est celui d'un site de l'État congolais fictif, à adapter par chaque entité.
"""

from .outils import accordeons, alerte, encadre, paragraphe

MENTIONS = [
    paragraphe(
        "<p class=\"sdcd-texte-lead\">Ce site est édité par le ministère du Numérique de la "
        "République Démocratique du Congo. Il présente Sites Conformes, le gestionnaire de "
        "contenus mis à disposition des services de l’État.</p>"
    ),
    alerte("Site de démonstration", "Les contenus, actualités, événements et coordonnées de ce site "
           "sont fictifs. Ils illustrent ce qu’un site public peut publier.", "info"),
    paragraphe(
        "<h2>Éditeur</h2>"
        "<p>Ministère du Numérique<br>Boulevard du 30 Juin, Kinshasa-Gombe<br>"
        "République Démocratique du Congo</p>"
        "<p>Directeur de la publication : le secrétaire général du ministère du Numérique.</p>"
        "<h2>Hébergement</h2>"
        "<p>Le site est hébergé en République Démocratique du Congo par l’Agence de "
        "développement du numérique, sur l’infrastructure de l’État. Les sauvegardes sont "
        "quotidiennes et conservées trente jours.</p>"
        "<h2>Conception et réalisation</h2>"
        "<p>Le site est construit avec Sites Conformes, logiciel libre publié sous licence "
        "AGPL-3.0, et le Système de design de l’État congolais. Son code source est public.</p>"
        "<h2>Propriété intellectuelle</h2>"
        "<p>Sauf mention contraire, les contenus de ce site sont placés sous la licence ouverte "
        "de l’État congolais : ils peuvent être réutilisés librement, à condition d’en citer "
        "la source et la date. Les armoiries de la République et les marques des services "
        "publics restent protégées et ne peuvent être réutilisées sans autorisation.</p>"
    ),
    paragraphe("<h2>Données personnelles</h2>"),
    accordeons("Vos données, en trois questions", [
        ("Quelles données sont collectées ?",
         "<p>Le formulaire de contact recueille le nom, l’adresse électronique, le numéro de "
         "téléphone et le message. Ces données servent uniquement à répondre à la demande.</p>"),
        ("Combien de temps sont-elles conservées ?",
         "<p>Les messages sont conservés douze mois après la réponse, puis supprimés. Les "
         "journaux techniques du serveur sont conservés un an, conformément à la loi.</p>"),
        ("Quels sont vos droits ?",
         "<p>Vous pouvez demander l’accès, la rectification ou la suppression de vos données "
         "en écrivant au délégué à la protection des données du ministère, par le formulaire "
         "de contact ou par courrier à l’adresse de l’éditeur. La réponse arrive sous un mois.</p>"),
    ], niveau="h3"),
    encadre("Cookies",
            "<p>Ce site n’utilise aucun cookie de mesure d’audience ni de publicité. Seuls des "
            "témoins techniques sont déposés : votre choix de thème d’affichage et, pour les "
            "agents connectés, la session du back-office. Ils ne sont transmis à personne.</p>",
            icone="ri-shield-check-line", couleur="chart-1"),
]

ACCESSIBILITE = [
    paragraphe(
        "<p class=\"sdcd-texte-lead\">Le ministère du Numérique s’engage à rendre ce site accessible "
        "à toutes les personnes, quelles que soient leurs capacités et les appareils qu’elles "
        "utilisent.</p>"
    ),
    paragraphe(
        "<h2>État de conformité</h2>"
        "<p>Ce site est <strong>partiellement conforme</strong> aux règles pour l’accessibilité des "
        "contenus web (WCAG 2.2, niveau AA), en raison des non-conformités listées ci-dessous.</p>"
        "<h2>Résultats des tests</h2>"
        "<p>L’audit réalisé en août 2026 sur un échantillon de dix pages relève un taux de "
        "conformité de 92 % des critères applicables. Les tests ont été menés avec un lecteur "
        "d’écran, au clavier seul, sur un téléphone et avec un agrandissement de 200 %.</p>"
        "<h2>Contenus non accessibles</h2>"
        "<ul><li>Les documents PDF publiés avant 2026 ne sont pas tous balisés ; ils sont "
        "remplacés au fil de leur mise à jour.</li>"
        "<li>Les vidéos intégrées n’ont pas toutes de transcription ; le bloc « transcription » "
        "du CMS permet de l’ajouter et les rédacteurs y sont formés.</li></ul>"
        "<h2>Établissement de cette déclaration</h2>"
        "<p>Cette déclaration a été établie le 3 septembre 2026. Les composants du Système de "
        "design de l’État congolais sont testés à chaque version ; les pages de ce site sont "
        "vérifiées automatiquement à chaque publication (contraste, alternatives, titres, "
        "cibles tactiles).</p>"
    ),
    encadre("Vous rencontrez une difficulté ?",
            "<p>Écrivez-nous par le formulaire de contact en indiquant la page concernée et le "
            "problème rencontré. Nous vous répondons sous deux jours ouvrés et proposons, si "
            "besoin, le contenu sous une autre forme.</p>",
            icone="ri-customer-service-2-line", couleur="chart-1"),
    paragraphe(
        "<h2>Voies de recours</h2>"
        "<p>Si vous n’obtenez pas de réponse satisfaisante, vous pouvez saisir le médiateur de "
        "la République ou le ministère du Numérique, direction des services aux usagers, "
        "boulevard du 30 Juin, Kinshasa-Gombe.</p>"
    ),
]
