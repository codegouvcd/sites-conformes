"""Documentation du site vitrine : creer son site, le systeme de design, la FAQ.

Contenu redige, repris tel quel de la premiere version de la commande.
"""

from wagtail.rich_text import RichText


def rt(html):
    return RichText(html)


# ------------------------------------------------------------- créer son site
def corps_creer():
    return [
        (
            "paragraph",
            rt(
                "<p class=\"sdcd-texte-lead\">De la demande d’ouverture à la mise en "
                "ligne, la création d’un site suit six étapes. Les trois premières "
                "relèvent de votre administration, les trois suivantes de votre "
                "équipe éditoriale.</p>"
            ),
        ),
        (
            "stepper",
            {
                "title": "Ouvrir le site",
                "heading_tag": "h2",
                "total": 6,
                "current": 1,
                "steps": [
                    (
                        "step",
                        {
                            "title": "Désigner un responsable de publication",
                            "detail": "C’est la personne qui engage l’entité sur ce qui est "
                            "publié. Elle figure dans les mentions légales et arbitre en "
                            "cas de doute. Sans elle, le site ne peut pas ouvrir.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Obtenir un nom de domaine en .gouv.cd",
                            "detail": "Le domaine est délivré par l’autorité compétente. "
                            "Un site d’État se reconnaît à son adresse : c’est la première "
                            "protection du citoyen contre les sites frauduleux.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Choisir l’hébergement",
                            "detail": "Hébergement par votre direction informatique, ou "
                            "délégué. Le CMS s’installe avec Docker et une base "
                            "PostgreSQL ; l’installation type tient sur un serveur modeste.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Renseigner la configuration du site",
                            "detail": "Intitulé officiel, sous-titre, logo de l’opérateur, "
                            "coordonnées. Tout se règle dans Configuration › Configuration "
                            "du site, sans toucher au code.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Écrire les pages obligatoires",
                            "detail": "Mentions légales, déclaration d’accessibilité, page "
                            "de contact. Elles existent déjà, vides : votre service "
                            "juridique en fournit le contenu applicable.",
                        },
                    ),
                    (
                        "step",
                        {
                            "title": "Construire l’arborescence et publier",
                            "detail": "Créez vos rubriques, assemblez vos pages à partir "
                            "des blocs, prévisualisez, publiez. Une page peut être "
                            "préparée puis publiée à une date choisie.",
                        },
                    ),
                ],
            },
        ),
        (
            "paragraph",
            rt(
                "<h2>Assembler une page</h2>"
                "<p>Une page se compose de blocs empilés. Vous choisissez un bloc, vous "
                "le remplissez, vous le déplacez si besoin. Il n’y a pas de gabarit figé "
                "à respecter : c’est la succession des blocs qui fait la page.</p>"
            ),
        ),
        (
            "accordions",
            [
                ("title", "Les blocs les plus utilisés"),
                (
                    "accordion",
                    {
                        "title": "Texte enrichi",
                        "content": rt(
                            "<p>Le bloc de base : titres, paragraphes, listes, liens, "
                            "gras et italique. Sa largeur de ligne est bornée "
                            "automatiquement, pour que le texte reste lisible sur un "
                            "grand écran.</p>"
                            "<p>Évitez de coller du texte depuis un traitement de texte "
                            "sans le nettoyer : la mise en forme importée entre en "
                            "conflit avec celle du système.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Cartes et tuiles",
                        "content": rt(
                            "<p>Une <strong>tuile</strong> oriente : elle porte un titre "
                            "court et mène ailleurs. Une <strong>carte</strong> informe : "
                            "elle porte un titre, une description, parfois une image, une "
                            "étiquette et un lien.</p>"
                            "<p>Posées dans une grille d’éléments, elles se réorganisent "
                            "d’elles-mêmes selon la largeur de l’écran.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Accordéons",
                        "content": rt(
                            "<p>Pour une suite de questions-réponses ou une procédure "
                            "détaillée. Le visiteur ouvre ce qui l’intéresse. À réserver "
                            "aux contenus secondaires : ce qui est replié est moins lu, "
                            "et n’est pas trouvé par la recherche du navigateur.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Fond pleine largeur",
                        "content": rt(
                            "<p>Pour marquer une rupture entre deux sections. Les "
                            "couleurs proposées sont des teintes claires, vérifiées pour "
                            "porter du texte sans perte de contraste.</p>"
                            "<p>Deux fonds colorés consécutifs annulent l’effet : "
                            "alternez avec du blanc.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Indicateur d’étapes",
                        "content": rt(
                            "<p>Pour une démarche en plusieurs temps, comme celle que "
                            "vous lisez plus haut. Indiquez le nombre total d’étapes et "
                            "l’étape en cours ; la jauge se dessine seule.</p>"
                        ),
                    },
                ),
            ],
        ),
        (
            "paragraph",
            rt(
                "<h2>Avant de publier</h2>"
                "<p>Quatre vérifications valent d’être faites sur chaque page, avant le "
                "premier clic sur « Publier ».</p>"
            ),
        ),
        (
            "item_grid",
            {
                "column_width": "6",
                "items": [
                    (
                        "card",
                        {
                            "title": "Un seul titre de niveau 1",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>C’est le titre de la page, posé automatiquement. Dans "
                                "vos blocs de texte, commencez donc au niveau 2, et ne "
                                "sautez pas de niveau.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Une alternative sur chaque image",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Décrivez ce que l’image apporte. Si elle est purement "
                                "décorative, cochez la case prévue : elle sera ignorée "
                                "par les lecteurs d’écran.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Des liens qui se comprennent seuls",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>« Consulter le décret » plutôt que « cliquez ici ». "
                                "Un utilisateur de lecteur d’écran parcourt souvent la "
                                "liste des liens, hors de leur phrase.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Un aperçu sur téléphone",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Le bouton « Aperçu » de l’éditeur propose les "
                                "largeurs mobile et bureau. La majorité de vos visiteurs "
                                "verra la première.</p>"
                            ),
                        },
                    ),
                ],
            },
        ),
    ]


# --------------------------------------------------------- système de design
def corps_design():
    return [
        (
            "paragraph",
            rt(
                "<p class=\"sdcd-texte-lead\">Le Système de design RDC fournit les "
                "couleurs, la typographie et les composants communs aux sites de l’État "
                "congolais. Le CMS s’appuie dessus : vous n’avez rien à en connaître pour "
                "l’utiliser, mais en comprendre les règles aide à faire de bons choix.</p>"
            ),
        ),
        (
            "paragraph",
            rt(
                "<h2>Trois principes</h2>"
                "<p>Ils expliquent la plupart des contraintes que vous rencontrerez dans "
                "l’éditeur.</p>"
            ),
        ),
        (
            "item_grid",
            {
                "column_width": "4",
                "items": [
                    (
                        "card",
                        {
                            "title": "La couleur porte un sens",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Le vert dit la réussite, l’orange l’avertissement, le "
                                "rouge l’erreur. C’est pourquoi la palette est courte : "
                                "une couleur choisie pour décorer brouille un message que "
                                "d’autres pages utilisent pour alerter.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Le contraste n’est pas négociable",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Chaque couple texte/fond est vérifié à 4,5:1 au "
                                "minimum, en thème clair comme en thème sombre. Les fonds "
                                "proposés dans l’éditeur sont ceux qui passent ce seuil.</p>"
                            ),
                        },
                    ),
                    (
                        "card",
                        {
                            "title": "Le téléphone d’abord",
                            "heading_tag": "h3",
                            "description": rt(
                                "<p>Les composants sont dessinés pour un écran étroit, "
                                "puis étendus. Une grille de trois colonnes devient une "
                                "colonne unique sans que vous ayez à le prévoir.</p>"
                            ),
                        },
                    ),
                ],
            },
        ),
        (
            "paragraph",
            rt(
                "<h2>Quelques composants</h2>"
                "<p>Voici, rendus par le système lui-même, des éléments que vous "
                "retrouverez dans l’éditeur.</p>"
            ),
        ),
        (
            "badges_list",
            [
                ("badge", {"text": "Nouveau", "color": "nouveau"}),
                ("badge", {"text": "En vigueur", "color": "succes"}),
                ("badge", {"text": "En consultation", "color": "info"}),
                ("badge", {"text": "Abrogé", "color": "erreur"}),
            ],
        ),
        (
            "tags_list",
            [
                ("tag", {"label": "Santé", "color": "chart-4"}),
                ("tag", {"label": "Éducation", "color": "chart-1"}),
                ("tag", {"label": "Infrastructures", "color": "chart-3"}),
                ("tag", {"label": "Numérique", "color": "chart-2"}),
            ],
        ),
        (
            "highlight",
            {
                "text": rt(
                    "<p>Une mise en exergue attire l’œil sur une phrase, sans lui donner "
                    "le poids d’un titre. À employer une fois par page au plus.</p>"
                ),
                "color": "chart-2",
                "size": "sdcd-texte-lg",
            },
        ),
        (
            "quote",
            {
                "quote": "Un service public en ligne doit être aussi accessible que son "
                "guichet : à tous, sans condition.",
                "author_name": "Principe directeur",
                "author_title": "Système de design RDC",
            },
        ),
        (
            "callout",
            {
                "title": "Le système est public",
                "heading_tag": "h2",
                "icon_class": "ri-git-repository-line",
                "text": rt(
                    "<p>Code, jetons de couleur et composants sont publiés sous licence "
                    "MIT. Les armoiries, la devise et le filet tricolore restent, eux, "
                    "réservés aux entités de l’État.</p>"
                ),
                "color": "chart-1",
            },
        ),
    ]


# ------------------------------------------------------------------- la FAQ
def corps_faq():
    return [
        (
            "paragraph",
            rt(
                "<p class=\"sdcd-texte-lead\">Les questions que se posent les services "
                "avant d’ouvrir un site. Si la vôtre n’y figure pas, la page de contact "
                "est faite pour ça.</p>"
            ),
        ),
        (
            "accordions",
            [
                ("title", "Ouvrir et héberger"),
                (
                    "accordion",
                    {
                        "title": "Combien coûte le CMS ?",
                        "content": rt(
                            "<p>Le logiciel est libre et gratuit. Les coûts sont ceux de "
                            "l’hébergement, du nom de domaine et du temps de vos agents. "
                            "Il n’y a ni licence, ni redevance, ni engagement.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Faut-il un développeur ?",
                        "content": rt(
                            "<p>Pour installer et maintenir l’hébergement, oui — une "
                            "personne à l’aise avec Docker et PostgreSQL. Pour créer et "
                            "publier des pages, non : l’éditeur ne demande aucune "
                            "compétence technique.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Peut-on reprendre un site existant ?",
                        "content": rt(
                            "<p>Les contenus doivent être ressaisis ou importés page par "
                            "page. C’est l’occasion de faire le tri : un site repris tel "
                            "quel reconduit ses pages mortes.</p>"
                        ),
                    },
                ),
            ],
        ),
        (
            "accordions",
            [
                ("title", "Contenu et responsabilités"),
                (
                    "accordion",
                    {
                        "title": "Qui est responsable de ce qui est publié ?",
                        "content": rt(
                            "<p>Le responsable de publication désigné par l’entité. Le "
                            "CMS fournit l’outil ; il ne se substitue pas à la "
                            "responsabilité éditoriale, qui reste entière.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Que doivent contenir les mentions légales ?",
                        "content": rt(
                            "<p>L’identité de l’éditeur, celle de l’hébergeur, le "
                            "responsable de publication, et le traitement des données "
                            "personnelles. Le texte applicable relève du droit congolais : "
                            "faites-le valider par votre service juridique. Le CMS "
                            "fournit la page, pas son contenu.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Le site est-il accessible aux personnes handicapées ?",
                        "content": rt(
                            "<p>Le système de design pose les bases : contrastes, "
                            "navigation au clavier, structure de titres, alternatives "
                            "d’images. Mais un site n’est accessible que si son contenu "
                            "l’est aussi. La déclaration d’accessibilité doit refléter un "
                            "audit réel, pas une intention.</p>"
                        ),
                    },
                ),
                (
                    "accordion",
                    {
                        "title": "Plusieurs personnes peuvent-elles rédiger ?",
                        "content": rt(
                            "<p>Oui. Chaque rédacteur a son compte, et une page peut être "
                            "soumise à relecture avant publication. L’historique conserve "
                            "qui a modifié quoi, et permet de revenir en arrière.</p>"
                        ),
                    },
                ),
            ],
        ),
    ]


INTRO = [
    (
        "paragraph",
        rt(
            "<p class=\"sdcd-texte-lead\">Tout ce qu’il faut savoir pour ouvrir et tenir un site "
            "de l’État avec Sites Conformes : la démarche, le système de design, les "
            "questions que se posent les services.</p>"
        ),
    ),
]

PAGES = [
    ("creer-votre-site", "Créer votre site", corps_creer, 1),
    ("systeme-de-design", "Le système de design", corps_design, 2),
    ("questions-frequentes", "Questions fréquentes", corps_faq, 3),
]
