"""Page d'accueil du site vitrine : ce que le CMS est, pour qui, et comment l'essayer."""

from .outils import (
    accordeons,
    actualites_recentes,
    bouton,
    carte,
    citation,
    encadre,
    etapier,
    evenements_recents,
    grille,
    hero_image_texte,
    paragraphe,
    rt,
    tuile,
)


def hero(images, pages):
    return [
        hero_image_texte(
            "Créez un site aux standards de l’État",
            "<p>Sites Conformes permet aux ministères, agences et services publics "
            "congolais de créer un site internet ou intranet conforme au Système de "
            "design de l’État, sans coder ni peser sur leur budget. Ce commun "
            "numérique repose sur le gestionnaire de contenus libre Wagtail.</p>",
            [
                bouton("Créer votre site", page=pages["creer-votre-site"], icone="ri-rocket-line", cote="gauche"),
                bouton("Nous contacter", page=pages["contact"], type_="sdcd-button sdcd-button--secondaire",
                       icone="ri-mail-line", cote="gauche"),
            ],
            images["hero-accueil"],
        )
    ]


def corps(images, pages, blog, agenda):
    return [
        paragraphe("<h2>Quatre bonnes raisons d’utiliser Sites Conformes</h2>"),
        grille([
            ("tile", tuile("Un site conforme au système de design",
                           "<p>Armoiries, filet tricolore, typographie et couleurs sont posés par "
                           "le système. Les règles d’accessibilité sont intégrées aux composants.</p>",
                           page=pages["systeme-de-design"], image=images["illustration-blocs"])),
            ("tile", tuile("Un site géré en autonomie",
                           "<p>Aucune compétence informatique n’est nécessaire pour publier et "
                           "mettre à jour. Une matinée suffit pour prendre l’outil en main.</p>",
                           page=pages["creer-votre-site"], image=images["illustration-redaction"])),
            ("tile", tuile("Un budget maîtrisé",
                           "<p>Le logiciel est libre et gratuit. Seuls l’hébergement et "
                           "l’éventuel accompagnement restent à la charge du service.</p>",
                           page=pages["questions-frequentes"], image=images["illustration-securite"])),
            ("tile", tuile("Un site sécurisé et hébergé où vous voulez",
                           "<p>Mises à jour de sécurité suivies, en-têtes de protection posés par "
                           "défaut, hébergement chez l’État ou chez un prestataire agréé.</p>",
                           page=pages["questions-frequentes"])),
        ], largeur="6"),

        paragraphe("<h2>Les principales fonctionnalités</h2>"),
        grille([
            ("card", carte("Blocs prêts à l’emploi",
                           "<p>Choisissez, assemblez et remplissez des composants préconfigurés : "
                           "texte, image, carte, accordéon, tableau, vidéo.</p>",
                           page=pages["composant-blocs"], fond_gris=True)),
            ("card", carte("Différents types de pages",
                           "<p>Pages de contenu, actualités, agenda, catalogue de services, "
                           "formulaires : chaque type a son gabarit et ses filtres.</p>",
                           page=pages["exemples"], fond_gris=True)),
            ("card", carte("Modèles",
                           "<p>Partez d’un modèle de page préconçu et adaptez-le : "
                           "atterrissage, site vitrine, page avec menu latéral.</p>",
                           page=pages["modeles"], fond_gris=True)),
            ("card", carte("Personnalisation",
                           "<p>Arborescence, menus, bandeau d’information, lettre "
                           "d’information, réseaux sociaux, thème sombre : tout se règle "
                           "dans le back-office.</p>",
                           page=pages["creer-votre-site"], fond_gris=True)),
            ("card", carte("Gestion collaborative",
                           "<p>Ajoutez des rédacteurs, définissez leurs droits, mettez en "
                           "place un circuit de validation avant publication.</p>",
                           page=pages["creer-votre-site"], fond_gris=True)),
            ("card", carte("Site public ou intranet",
                           "<p>Publiez pour tous, réservez l’accès aux agents connectés, ou "
                           "installez le site sur le réseau interne de votre entité.</p>",
                           page=pages["questions-frequentes"], fond_gris=True)),
        ], largeur="4"),

        paragraphe(
            "<h2>Les cas d’usage</h2>"
            "<ul>"
            "<li>Présenter un ministère, ses services et son actualité, avec un <b>site vitrine</b>.</li>"
            "<li>Accueillir les usagers d’un service en ligne et recueillir leurs demandes, "
            "avec une <b>page d’atterrissage</b> et un <b>formulaire</b>.</li>"
            "<li>Informer le public des actualités et des rendez-vous d’une administration, "
            "avec un <b>blog</b> et un <b>agenda</b>.</li>"
            "<li>Recenser une offre de services ou de démarches, avec un <b>catalogue</b>.</li>"
            "<li>Diffuser des informations internes aux agents, sur un <b>intranet</b>.</li>"
            "</ul>"
        ),

        paragraphe("<h2>Des exemples pour chaque cas</h2>"
                   "<p>Chaque exemple ci-dessous est une page de ce site, construite avec les "
                   "blocs du CMS. Ouvrez-la, puis retrouvez-la dans le back-office pour voir "
                   "comment elle est faite.</p>"),
        grille([
            ("card", carte("Site vitrine d’une administration",
                           "<p>Actualités à la une, services principaux, informations par type "
                           "d’usager.</p>", page=pages["site-vitrine"], image=images["hero-vitrine"],
                           ratio="sdcd-ratio-16x9", badge="Site vitrine")),
            ("card", carte("Page d’atterrissage d’un service",
                           "<p>Une promesse, trois arguments, des cas d’usage et un appel à "
                           "l’action.</p>", page=pages["page-atterrissage"], image=images["hero-atterrissage"],
                           ratio="sdcd-ratio-16x9", badge="Atterrissage")),
            ("card", carte("Actualités",
                           "<p>Articles classés par catégorie et par étiquette, flux RSS et "
                           "Atom.</p>", page=blog, image=images["actualite-numerique"],
                           ratio="sdcd-ratio-16x9", badge="Blog")),
            ("card", carte("Agenda",
                           "<p>Événements filtrables par date et par catégorie, export vers "
                           "votre calendrier.</p>", page=agenda, image=images["evenement-conference"],
                           ratio="sdcd-ratio-16x9", badge="Agenda")),
            ("card", carte("Catalogue de services",
                           "<p>Des fiches classées par étiquette, générées à partir des "
                           "sous-pages.</p>", page=pages["catalogue-de-services"], image=images["service-passeport"],
                           ratio="sdcd-ratio-16x9", badge="Catalogue")),
            ("card", carte("Formulaire",
                           "<p>Tous les types de champs, réponses consultables dans le "
                           "back-office.</p>", page=pages["formulaire-de-demonstration"], image=images["illustration-redaction"],
                           ratio="sdcd-ratio-16x9", badge="Formulaire")),
        ], largeur="4"),

        encadre(
            "Puis-je utiliser Sites Conformes ?",
            "<p>Sites Conformes s’adresse aux institutions, ministères, agences et "
            "services de l’État congolais, et aux personnes qui y travaillent. Le "
            "Système de design de l’État représente son identité numérique : son usage "
            "est réservé aux sites officiels, en <b>.gouv.cd</b>. Il ne s’adresse pas "
            "aux particuliers, aux entreprises ni aux associations.</p>",
            icone="ri-shield-check-line", couleur="chart-2",
        ),

        paragraphe("<h2>Envie de tester ?</h2>"
                   "<p>Découvrez l’outil et faites vos essais pour déterminer s’il répond à "
                   "votre besoin. Un bac à sable est mis à disposition des équipes qui "
                   "souhaitent essayer Sites Conformes sans l’installer sur un serveur. Pour "
                   "y accéder, vous devez travailler pour l’État et votre projet doit être "
                   "éligible au système de design.</p>"),
        ("buttons_list", {"buttons": [
            ("button", bouton("Demander un accès au bac à sable", page=pages["contact"],
                              icone="ri-key-2-line", cote="gauche")),
            ("button", bouton("Voir le code source", url="https://github.com/codegouvcd/sites-conformes",
                              type_="sdcd-button sdcd-button--secondaire", icone="ri-github-line", cote="gauche")),
        ], "position": ""}),

        paragraphe("<h2>Un commun numérique pour des sites publics conformes</h2>"
                   "<p>Sites Conformes repose sur un socle libre déjà éprouvé, le gestionnaire "
                   "de contenus Wagtail, écrit en Python avec Django et maintenu par une large "
                   "communauté. La version congolaise y ajoute le Système de design de l’État, "
                   "des gabarits accessibles et des réglages de sécurité posés par défaut.</p>"
                   "<p>La force du commun : chaque amélioration, chaque correction bénéficie "
                   "à l’ensemble des administrations utilisatrices. Les évolutions du système "
                   "de design, les nouvelles fonctionnalités et les correctifs de sécurité "
                   "sont disponibles pour tous les sites à la mise à jour suivante.</p>"),
        citation(
            "Un service public en ligne doit être aussi accessible que son guichet : à "
            "tous, sans condition, depuis un téléphone comme depuis un bureau.",
            "Principe directeur", "Système de design de l’État congolais", image=images["portrait-agente"],
        ),

        accordeons("Questions fréquentes", [
            ("Quelles compétences faut-il pour utiliser Sites Conformes ?",
             "<p>Savoir rédiger et organiser un contenu. La mise en page se fait en "
             "assemblant des blocs ; aucune ligne de code n’est nécessaire.</p>"),
            ("Comment démarrer ?",
             "<p>Lisez le guide <i>Créer votre site</i> : six étapes, de la demande "
             "d’ouverture à la mise en ligne. Puis demandez un accès au bac à sable.</p>"),
            ("Comment héberger mon site ?",
             "<p>Chez l’hébergeur de l’État ou chez un prestataire agréé. Le site "
             "s’installe avec Docker ; la base de données et les fichiers restent la "
             "propriété de votre entité.</p>"),
            ("Le site sera-t-il accessible aux personnes handicapées ?",
             "<p>Les composants respectent les critères d’accessibilité (contrastes, "
             "clavier, lecteurs d’écran). La conformité finale dépend aussi des contenus : "
             "alternatives d’images, titres hiérarchisés, liens explicites.</p>"),
            ("Peut-on personnaliser un site ?",
             "<p>Menus, bandeau, lettre d’information, réseaux sociaux, thème, logo "
             "d’opérateur : tout se règle dans le back-office. Les couleurs et la "
             "typographie, elles, sont celles de l’État et ne se modifient pas.</p>"),
            ("Il manque une fonctionnalité, comment faire ?",
             "<p>Ouvrez une demande sur le dépôt de code ou écrivez-nous via la page de "
             "contact. Les besoins communs à plusieurs administrations sont priorisés.</p>"),
        ]),

        etapier("Feuille de route", 3, 2, [
            ("Portage du système de design de l’État",
             "Composants, couleurs, typographie et gabarits remplacés par ceux de la RDC."),
            ("Ouverture aux premiers services",
             "Bac à sable, accompagnement des premières entités, retours d’usage."),
            ("Généralisation",
             "Catalogue d’instances, hébergement mutualisé, formation des rédacteurs."),
        ]),

        actualites_recentes(blog),
        evenements_recents(agenda),
    ]


def description():
    return rt("<p>Sites Conformes est mis à disposition des services de l’État congolais. "
              "Le code est libre ; chaque entité reste responsable de ce qu’elle publie.</p>")
