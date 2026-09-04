"""Rubrique « Exemples » : une page par cas d'usage, en contexte congolais.

Chaque fonction renvoie ce qu'il faut pour construire la page : titre, corps,
en-tete, et le cas echeant les entrees (articles, evenements, fiches).
"""

from datetime import datetime, timezone

from .outils import (
    accordeons,
    actualites_recentes,
    alerte,
    badges,
    bouton,
    boutons,
    carte,
    citation,
    colonnes,
    encadre,
    etapier,
    etiquettes,
    evenements_recents,
    fiche_contact,
    fond,
    grille,
    hero_bandeau,
    hero_fond_image,
    image_texte,
    mise_en_avant,
    onglets,
    paragraphe,
    rt,
    tuile,
)

# Resumes (search_description) : ce que les catalogues et les partages affichent.
RESUMES = {
    "exemples": "Des pages construites avec les blocs du CMS, à ouvrir puis à retrouver dans le back-office.",
    "documentation": "La démarche pour ouvrir un site, le système de design, les questions fréquentes.",
    "creer-votre-site": "Six étapes, de la demande d’ouverture à la mise en ligne.",
    "systeme-de-design": "Couleurs, typographie et composants communs aux sites de l’État congolais.",
    "questions-frequentes": "Hébergement, nom de domaine, accessibilité, responsabilités de chacun.",
    "composants": "Chaque bloc du CMS dans toutes ses variantes : tuiles, cartes, accordéons, étapiers, mises en valeur.",
    "tuiles": "Tuiles simples, avec lien, badge, tag ou texte de détail, horizontales ou verticales.",
    "en-tetes-et-bandeaux": "En-têtes de page avec image, sur fond de couleur, et bandeaux d’appel à l’action.",
    "onglets-colonnes-et-fiches-contact": "Onglets, colonnes de largeur réglable et fiches contact.",
    "page-de-contenu-avec-menu-lateral": "Une page longue avec un menu latéral qui suit la lecture.",
    "blocs-simples-de-textes-et-dimages": "Paragraphes, images, vidéos, citations et boutons : les blocs de base.",
    "options-de-mise-en-valeur-de-textes": "Mises en avant, alertes, encadrés, badges et étiquettes.",
    "grilles-delements": "Grilles de tuiles, de cartes ou de blocs libres, en deux, trois ou quatre colonnes.",
    "accordeons": "Accordéons simples et groupés, ouverts ou fermés au chargement.",
    "cartes": "Cartes verticales et horizontales, avec image, badge, étiquettes ou fond gris.",
    "etapiers": "L’étapier : où l’on en est dans une démarche, et ce qu’il reste à faire.",
    "page-atterrissage": "Une promesse, trois arguments, des cas d’usage et un appel à l’action : le modèle d’un service en ligne.",
    "site-vitrine": "Actualités à la une, services principaux, informations par type d’usager : le modèle d’un ministère.",
    "actualites": "Articles classés par catégorie et par étiquette, flux RSS et Atom.",
    "agenda": "Ateliers, conférences, concertations et formations, filtrables par date et par catégorie.",
    "catalogue-de-services": "Des fiches classées par étiquette, générées à partir des sous-pages.",
    "formulaire-de-demonstration": "Tous les types de champs d’un formulaire, réponses consultables dans le back-office.",
    "acte-de-naissance": "Déclarer une naissance et obtenir l’acte, en ligne ou au guichet, gratuitement dans les 90 jours.",
    "passeport-biometrique": "Demander un passeport sur rendez-vous, avec un acte de naissance et une carte d’électeur.",
    "creer-son-entreprise": "Immatriculation, identification nationale et numéro d’impôt en un dossier, sous trois jours.",
    "declarer-ses-impots": "Déclarer la TVA et l’impôt professionnel en ligne, payer par virement ou par mobile.",
    "dorsale-nationale-goma": "Le tronçon Bukavu – Goma de la fibre nationale est en service.",
    "kikwit-site-en-une-semaine": "Deux agents, une journée de formation, un modèle de site vitrine.",
    "accessibilite-premiers-audits": "Dix sites ministériels audités : alternatives d’images, contrastes, PDF.",
    "un-site-public-doit-se-lire-au-telephone": "Neuf visites sur dix se font depuis un téléphone : concevoir pour lui d’abord.",
    "atelier-prise-en-main": "Une journée pour créer un site de démonstration, douze places.",
    "conference-services-publics-en-ligne": "Bilan du programme et feuille de route 2027, retransmis en direct.",
    "concertation-lubumbashi": "Deux jours d’ateliers avec usagers, agents et associations.",
    "formation-redacteurs-en-ligne": "Trois heures pour écrire court, hiérarchiser ses titres, décrire ses images.",
}

# ----------------------------------------------------------------- Exemples
INTRO_EXEMPLES = [
    paragraphe(
        "<p class=\"sdcd-texte-lead\">Chaque exemple est une page de ce site, construite "
        "avec les blocs du CMS et rien d’autre. Ouvrez-la, puis retrouvez-la dans le "
        "back-office pour voir comment elle est assemblée.</p>"
        "<p>Les exemples de pages montrent un cas d’usage complet : page d’atterrissage, "
        "site vitrine, blog, agenda, catalogue, formulaire. Les exemples de composants, "
        "regroupés dans les modèles de pages à copier, montrent chaque bloc dans "
        "toutes ses variantes.</p>"
    ),
]


INTRO_COMPOSANTS = [
    paragraphe(
        "<p class=\"sdcd-texte-lead\">Chaque page ci-dessous montre un bloc du CMS dans toutes ses "
        "variantes, tel qu’un rédacteur peut l’assembler depuis le back-office.</p>"
        "<p>Chaque page dit où trouver le bloc dans le back-office. Pour repartir d’une page "
        "complète, les modèles de pages à copier sont dans le back-office, rubrique « Pages ».</p>"
    ),
]


# ------------------------------------------------------ page d'atterrissage
def atterrissage(images, pages):
    hero = [
        hero_fond_image(
            "Déclarez la naissance de votre enfant en ligne",
            "<p>Un service du ministère de l’Intérieur pour obtenir l’acte de naissance "
            "sans file d’attente : la demande se fait depuis un téléphone, le retrait "
            "au bureau d’état civil de votre commune.</p>",
            [
                bouton("Commencer la démarche", page=pages["formulaire-de-demonstration"],
                       icone="ri-arrow-right-line", cote="droite"),
                bouton("Comment ça marche", page=pages["creer-votre-site"],
                       type_="sdcd-button sdcd-button--secondaire"),
            ],
            images["hero-atterrissage"],
        )
    ]
    corps = [
        colonnes("Trois raisons d’utiliser ce service", [
            ("4", [("text", rt("<h3>Sans déplacement</h3><p>La demande se fait en ligne, en dix "
                              "minutes. Vous ne vous déplacez qu’une fois, pour le retrait.</p>")),
                   ("link", {"text": "En savoir plus", "link_type": "page", "page": pages["questions-frequentes"],
                             "icon": "ri-arrow-right-line sdcd-lien--icone-droite"})]),
            ("4", [("text", rt("<h3>Suivi par SMS</h3><p>Vous recevez un message à chaque étape : "
                              "réception, vérification, acte prêt.</p>")),
                   ("link", {"text": "En savoir plus", "link_type": "page", "page": pages["questions-frequentes"],
                             "icon": "ri-arrow-right-line sdcd-lien--icone-droite"})]),
            ("4", [("text", rt("<h3>Gratuit</h3><p>La déclaration dans les 90 jours est gratuite. "
                              "Passé ce délai, un jugement supplétif est nécessaire.</p>")),
                   ("link", {"text": "En savoir plus", "link_type": "page", "page": pages["questions-frequentes"],
                             "icon": "ri-arrow-right-line sdcd-lien--icone-droite"})]),
        ], couleur="gris"),

        paragraphe("<h2>Les cas d’usage</h2>"),
        grille([
            ("card", carte("Naissance à la maternité",
                           "<p>La maternité transmet la déclaration ; vous n’avez qu’à confirmer "
                           "les prénoms et retirer l’acte.</p>",
                           image=images["service-etat-civil"], ratio="sdcd-ratio-16x9",
                           etiquettes=("Naissance", "Kinshasa"))),
            ("card", carte("Naissance à domicile",
                           "<p>Deux témoins majeurs et la carte d’électeur d’un parent "
                           "suffisent pour déclarer.</p>",
                           image=images["service-etat-civil"], ratio="sdcd-ratio-16x9",
                           etiquettes=("Naissance", "Provinces"))),
            ("card", carte("Déclaration tardive",
                           "<p>Au-delà de 90 jours, la démarche passe par le tribunal de paix. "
                           "Le service prépare le dossier.</p>",
                           image=images["service-passeport"], ratio="sdcd-ratio-16x9",
                           etiquettes=("Jugement supplétif",))),
            ("card", carte("Copie d’un acte existant",
                           "<p>Pour un passeport, une inscription scolaire ou un mariage, "
                           "demandez une copie certifiée.</p>",
                           image=images["service-impots"], ratio="sdcd-ratio-16x9",
                           etiquettes=("Copie", "En ligne"))),
        ], largeur="6"),

        etapier("Votre démarche en quatre étapes", 4, 1, [
            ("Remplir la demande", "Identité des parents, lieu et date de naissance, prénoms de l’enfant."),
            ("Joindre les pièces", "Attestation de naissance, pièce d’identité d’un parent."),
            ("Vérification", "L’officier d’état civil contrôle le dossier sous cinq jours ouvrés."),
            ("Retrait de l’acte", "Au bureau d’état civil de la commune, sur présentation du récépissé."),
        ]),

        fond([
            ("text", rt("<h2>Un service qui s’adresse à tous</h2>"
                        "<p>Le service est conçu pour être utilisé depuis un téléphone, avec une "
                        "connexion lente, par des personnes qui n’ont jamais fait de démarche en "
                        "ligne. Les textes sont courts, les étapes sont annoncées, l’aide est "
                        "disponible en français, lingala, swahili, kikongo et tshiluba.</p>")),
            ("buttons_list", {"buttons": [("button", bouton("Commencer la démarche",
                                                            page=pages["formulaire-de-demonstration"]))],
                              "position": ""}),
        ], couleur="bleu"),

        paragraphe("<h2>Ils ont utilisé le service</h2>"),
        citation("J’ai déclaré la naissance de ma fille depuis Matadi, en dix minutes, et j’ai "
                 "retiré l’acte le lundi suivant. Personne ne m’a demandé un franc.",
                 "Pascaline M.", "Mère de famille, Kongo-Central", image=images["portrait-agente"]),

        paragraphe("<h2>Une question ?</h2>"),
        grille([
            ("contact_card", fiche_contact("Service de l’état civil", "Assistance aux usagers",
                                           "Ministère de l’Intérieur, Sécurité et Affaires coutumières",
                                           "<p>Du lundi au vendredi, 8 h – 16 h<br>"
                                           "<a href=\"tel:+243000000000\">+243 000 000 000</a></p>",
                                           image=images["portrait-agent"], etiquettes_=("Kinshasa", "Gombe"))[1]),
        ], largeur="6"),
    ]
    return hero, corps


# ------------------------------------------------- site vitrine d'une administration
def vitrine(images, pages, blog, agenda):
    hero = [
        hero_bandeau(
            "Ministère du Numérique",
            "<p>Le ministère conduit la transformation numérique de l’État et de "
            "l’économie congolaise : connectivité, services publics en ligne, "
            "protection des données, formation.</p>",
            [
                bouton("Nos services", page=pages["catalogue-de-services"]),
                bouton("Nous contacter", page=pages["contact"], type_="sdcd-button sdcd-button--secondaire"),
            ],
            images["hero-vitrine"],
            haut=4,  # sans marge, le titre collait au bandeau d'information
        )
    ]
    corps = [
        actualites_recentes(blog, "Les actualités à la une", 4),

        fond([
            ("text", rt("<h2>Les principaux services du ministère</h2>")),
            ("item_grid", {"column_width": "6", "horizontal_align": "left", "vertical_align": "", "items": [
                ("card", carte("Guichet unique des démarches",
                               "<p>Un point d’entrée pour les démarches administratives en ligne : "
                               "état civil, passeport, entreprises, impôts.</p>",
                               page=pages["catalogue-de-services"], image=images["service-passeport"],
                               ratio="sdcd-ratio-16x9")),
                ("card", carte("Programme Connectivité",
                               "<p>Raccorder les chefs-lieux de province à la dorsale nationale et "
                               "équiper les écoles et centres de santé.</p>",
                               page=pages["page-atterrissage"], image=images["actualite-numerique"],
                               ratio="sdcd-ratio-16x9")),
                ("card", carte("Protection des données",
                               "<p>Accompagner les administrations et les entreprises dans "
                               "l’application de la loi sur les données personnelles.</p>",
                               page=pages["questions-frequentes"], image=images["illustration-securite"],
                               ratio="sdcd-ratio-16x9")),
                ("card", carte("Académie du numérique",
                               "<p>Former les agents de l’État aux outils numériques, du "
                               "traitement de texte à la gestion de projet.</p>",
                               page=agenda, image=images["actualite-formation"],
                               ratio="sdcd-ratio-16x9")),
            ]}),
        ], couleur="gris"),

        paragraphe("<h2>Des informations adaptées à chaque public</h2>"),
        onglets(
            ("Citoyens", [
                ("text", rt("<p>Retrouvez les démarches en ligne, les points d’accès numérique "
                            "dans votre province et les conseils pour protéger vos données. "
                            "L’assistance est joignable par téléphone et par WhatsApp.</p>")),
                ("quote", {"quote": "Le numérique doit rapprocher l’administration du citoyen, "
                                    "pas ajouter une file d’attente.",
                           "author_name": "Direction des services aux usagers", "author_title": "Ministère du Numérique",
                           "color": "chart-1"}),
                ("buttons_list", {"buttons": [("button", bouton("Voir les démarches",
                                                                page=pages["catalogue-de-services"]))],
                                  "position": ""}),
            ]),
            ("Entreprises", [
                ("text", rt("<p>Création d’entreprise en ligne au guichet unique, agrément des "
                            "opérateurs, appels à projets et incubateurs soutenus par le ministère. "
                            "Les start-up labellisées bénéficient d’un accompagnement dédié.</p>")),
                ("buttons_list", {"buttons": [("button", bouton("Créer son entreprise",
                                                                page=pages["catalogue-de-services"]))],
                                  "position": ""}),
            ]),
            ("Administrations", [
                ("text", rt("<p>Sites Conformes, messagerie de l’État, identité numérique des "
                            "agents, hébergement mutualisé : les services communs sont ouverts à "
                            "toutes les entités publiques sur simple demande.</p>")),
                ("buttons_list", {"buttons": [("button", bouton("Créer votre site",
                                                                page=pages["creer-votre-site"]))],
                                  "position": ""}),
            ]),
        ),

        evenements_recents(agenda, "Prochains rendez-vous", 3),

        paragraphe("<h2>Où nous trouver</h2>"),
        image_texte(images["hero-vitrine"],
                    "<p><b>Ministère du Numérique</b><br>Boulevard du 30 Juin, Kinshasa-Gombe<br>"
                    "Du lundi au vendredi, 8 h – 16 h</p>"
                    "<p>Accès : arrêt « Gare centrale », lignes 1 et 4. Le bâtiment est accessible "
                    "aux personnes à mobilité réduite par l’entrée sud.</p>",
                    cote="left", largeur="5"),
    ]
    return hero, corps


# ------------------------------------------------------------------- blog
CATEGORIES_BLOG = ["Actualité", "Retour d’expérience", "Tribune"]
CATEGORIES_AGENDA = ["Atelier", "Conférence", "Concertation", "Formation"]


def articles(images):
    """(slug, titre, date, categorie, etiquettes, image, corps)."""
    return [
        ("dorsale-nationale-goma", "La dorsale nationale atteint Goma",
         datetime(2026, 8, 24, 9, 0, tzinfo=timezone.utc), "Actualité", ["Numérique", "Goma"],
         images["actualite-numerique"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Le tronçon Bukavu – Goma de la fibre optique "
                        "nationale est en service. Les administrations provinciales du Nord-Kivu "
                        "disposent d’une connexion stable pour leurs services en ligne.</p>"
                        "<p>Le raccordement concerne d’abord le gouvernorat, l’hôpital provincial et "
                        "l’université. Les écoles suivront au premier trimestre 2027. Le ministère "
                        "rappelle que les sites publics de la province peuvent être ouverts avec "
                        "Sites Conformes sans hébergement local.</p>"),
             mise_en_avant("<p>1 200 km de fibre posés depuis 2024, 6 chefs-lieux raccordés.</p>"),
         ]),
        ("kikwit-site-en-une-semaine", "Comment la mairie de Kikwit a ouvert son site en une semaine",
         datetime(2026, 8, 12, 10, 0, tzinfo=timezone.utc), "Retour d’expérience", ["Formation", "Kwilu"],
         images["actualite-formation"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Deux agents, une formation d’une journée et "
                        "un modèle de site vitrine : la mairie publie ses avis et ses horaires "
                        "depuis le 10 août.</p>"
                        "<p>« Nous avons commencé par les pages obligatoires, puis les actualités. "
                        "Le plus long a été de rassembler les textes », explique la chargée de "
                        "communication. Le site tourne sur l’hébergement mutualisé de l’État.</p>"),
             etapier("Leur parcours", 3, 3, [
                 ("Formation", "Une journée, à distance."),
                 ("Contenus", "Trois jours pour écrire et relire."),
                 ("Mise en ligne", "Une matinée, avec l’équipe Sites Conformes."),
             ]),
         ]),
        ("accessibilite-premiers-audits", "Accessibilité : les premiers audits des sites de l’État",
         datetime(2026, 7, 30, 9, 0, tzinfo=timezone.utc), "Actualité", ["Accessibilité"],
         images["actualite-accessibilite"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Dix sites ministériels ont été audités en "
                        "juin. Les défauts les plus fréquents : images sans alternative, "
                        "contrastes insuffisants, documents PDF non balisés.</p>"
                        "<p>Les sites construits avec Sites Conformes obtiennent les meilleurs "
                        "résultats sur la navigation au clavier et les contrastes, posés par le "
                        "système de design. Le travail reste à faire sur les contenus.</p>"),
             alerte("À retenir", "<p>Chaque image publiée doit porter une alternative textuelle. "
                                 "Le CMS la demande à l’import.</p>", "info"),
         ]),
        ("un-site-public-doit-se-lire-au-telephone", "Un site public doit se lire au téléphone",
         datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc), "Tribune", ["Numérique", "Accessibilité"],
         images["actualite-tribune"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Plus de neuf visites sur dix des sites publics "
                        "congolais se font depuis un téléphone, souvent en 3G. Concevoir pour "
                        "l’écran d’un bureau, c’est concevoir pour une minorité.</p>"
                        "<p>Une page légère, des textes courts, des images qui se recadrent, des "
                        "boutons assez grands pour un pouce : ce ne sont pas des options. Le "
                        "système de design de l’État les impose ; il reste aux rédacteurs à ne pas "
                        "les défaire par des contenus trop lourds.</p>"),
             citation("Le meilleur site de l’État est celui qui s’ouvre en moins de trois secondes "
                      "sur un téléphone d’entrée de gamme.", "Direction du numérique de l’État",
                      "Tribune"),
         ]),
    ]


def evenements(images):
    """(slug, titre, debut, fin, lieu, categorie, etiquettes, image, corps)."""
    return [
        ("atelier-prise-en-main", "Atelier de prise en main de Sites Conformes",
         datetime(2026, 10, 6, 8, 0, tzinfo=timezone.utc), datetime(2026, 10, 6, 15, 0, tzinfo=timezone.utc),
         "Académie du numérique, Kinshasa", "Atelier", ["Kinshasa", "Formation"], images["evenement-atelier"], [
             paragraphe("<p>Une journée pour créer un site de démonstration : pages, menus, "
                        "actualités, formulaire. Apportez vos textes et votre logo. Places "
                        "limitées à douze agents ; inscription obligatoire.</p>"),
             badges("Gratuit", "Sur inscription"),
         ]),
        ("conference-services-publics-en-ligne", "Conférence : services publics en ligne, où en est la RDC ?",
         datetime(2026, 10, 22, 9, 0, tzinfo=timezone.utc), datetime(2026, 10, 22, 12, 0, tzinfo=timezone.utc),
         "Palais du Peuple, Kinshasa", "Conférence", ["Kinshasa"], images["evenement-conference"], [
             paragraphe("<p>Bilan des deux premières années du programme, témoignages de "
                        "provinces, présentation de la feuille de route 2027. Retransmission en "
                        "direct pour les provinces.</p>"),
         ]),
        ("concertation-lubumbashi", "Concertation avec les usagers du guichet unique",
         datetime(2026, 11, 12, 9, 0, tzinfo=timezone.utc), datetime(2026, 11, 13, 16, 0, tzinfo=timezone.utc),
         "Hôtel de ville, Lubumbashi", "Concertation", ["Lubumbashi"], images["evenement-concertation"], [
             paragraphe("<p>Deux jours d’ateliers avec des usagers, des agents et des "
                        "associations pour améliorer les démarches d’état civil et de "
                        "passeport. Les conclusions seront publiées ici.</p>"),
         ]),
        ("formation-redacteurs-en-ligne", "Formation en ligne : rédiger pour le web public",
         datetime(2026, 12, 3, 8, 0, tzinfo=timezone.utc), datetime(2026, 12, 3, 11, 0, tzinfo=timezone.utc),
         "En ligne", "Formation", ["En ligne", "Formation"], images["evenement-formation"], [
             paragraphe("<p>Trois heures pour apprendre à écrire court, hiérarchiser ses titres "
                        "et décrire ses images. Ouvert à tous les agents ; lien de connexion "
                        "envoyé la veille.</p>"),
             badges("En ligne", "Gratuit"),
         ]),
    ]


def intro_blog():
    return [
        paragraphe("<p class=\"sdcd-texte-lead\">Les actualités du programme Sites Conformes et "
                   "des services numériques de l’État. Filtrez par catégorie ou par étiquette ; "
                   "abonnez-vous au flux RSS pour ne rien manquer.</p>"),
    ]


def intro_agenda():
    return [
        paragraphe("<p class=\"sdcd-texte-lead\">Ateliers, conférences, concertations et formations "
                   "à venir. Filtrez par date ou par catégorie, et ajoutez un événement à votre "
                   "calendrier.</p>"),
    ]


# -------------------------------------------------------------- catalogue
def fiches(images):
    """(slug, titre, etiquettes, image, corps)."""
    return [
        ("acte-de-naissance", "Demander un acte de naissance", ["État civil", "Gratuit", "En ligne"],
         images["service-etat-civil"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Déclaration dans les 90 jours suivant la naissance, "
                        "au bureau d’état civil de la commune ou en ligne.</p>"),
             etapier("La démarche", 3, 1, [
                 ("Déclarer", "En ligne ou au guichet, avec l’attestation de la maternité."),
                 ("Vérifier", "L’officier d’état civil contrôle le dossier sous cinq jours."),
                 ("Retirer", "L’acte est remis au guichet, sur récépissé."),
             ]),
             accordeons("Questions", [
                 ("Que faire après 90 jours ?", "<p>Un jugement supplétif du tribunal de paix est nécessaire."),
                 ("Combien ça coûte ?", "<p>La déclaration dans les délais est gratuite.</p>"),
             ], niveau="h2"),
         ]),
        ("passeport-biometrique", "Obtenir un passeport biométrique", ["Identité", "Payant", "Sur rendez-vous"],
         images["service-passeport"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Le passeport se demande sur rendez-vous dans "
                        "un centre d’enrôlement, avec un acte de naissance et une carte "
                        "d’électeur.</p>"
                        "<p>Délai indicatif : trois semaines à Kinshasa, cinq en province. Le "
                        "paiement se fait par voie bancaire ou mobile, jamais en espèces au "
                        "guichet.</p>"),
             alerte("Attention aux intermédiaires", "<p>Seuls les centres officiels délivrent des "
                    "passeports. Aucun intermédiaire n’est habilité.</p>", "warning"),
         ]),
        ("creer-son-entreprise", "Créer son entreprise au guichet unique", ["Entreprises", "En ligne", "Payant"],
         images["service-entreprise"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Le Guichet unique de création d’entreprise "
                        "réunit en un dossier l’immatriculation au registre du commerce, "
                        "l’identification nationale et le numéro d’impôt.</p>"
                        "<p>Délai : trois jours ouvrés après dépôt du dossier complet. Les "
                        "statuts type sont fournis pour les sociétés à responsabilité limitée.</p>"),
             etiquettes("SARL", "SA", "Entreprise individuelle"),
         ]),
        ("declarer-ses-impots", "Déclarer et payer ses impôts en ligne", ["Impôts", "En ligne", "Entreprises"],
         images["service-impots"], [
             paragraphe("<p class=\"sdcd-texte-lead\">Les entreprises déclarent la TVA et l’impôt "
                        "professionnel sur le portail de la Direction générale des impôts, "
                        "et paient par virement ou par mobile.</p>"
                        "<p>Les particuliers salariés n’ont pas de déclaration à faire : l’impôt "
                        "est retenu à la source par l’employeur.</p>"),
             encadre("Calendrier", "<p>TVA : le 15 de chaque mois. Impôt professionnel : "
                     "acomptes en août et en décembre, solde au 31 mars.</p>", icone="ri-calendar-line", niveau="h2"),
         ]),
    ]


def intro_catalogue():
    return [
        paragraphe("<p class=\"sdcd-texte-lead\">Un catalogue se remplit tout seul : chaque page "
                   "publiée sous cet index y apparaît sous forme de tuile, avec l’image d’en-tête "
                   "et les étiquettes qu’on lui a données. Les filtres se construisent à partir "
                   "des étiquettes.</p>"),
    ]


# -------------------------------------------------------------- formulaire
def champs_formulaire():
    """Un champ par type disponible, dans l'ordre des choix du CMS."""
    return [
        ("singleline", "Votre nom", "Utilisez ce champ pour une réponse courte.", True, ""),
        ("multiline", "Votre message", "Utilisez ce champ pour une réponse longue.", True, ""),
        ("email", "Votre adresse électronique", "Format attendu : nom@domaine.cd", True, ""),
        ("number", "Nombre d’agents dans votre service", "Un nombre entier.", False, ""),
        ("url", "Adresse de votre site actuel", "Format attendu : https://www.domaine.gouv.cd", False, ""),
        ("checkbox", "J’accepte d’être recontacté", "Une case à cocher pour un consentement.", False, ""),
        ("checkboxes", "Ce qui vous intéresse", "Plusieurs réponses possibles.", False,
         "Site vitrine, Actualités, Agenda, Catalogue, Formulaires"),
        ("dropdown", "Votre province", "Une réponse parmi une liste.", False,
         "Kinshasa, Kongo-Central, Haut-Katanga, Nord-Kivu, Sud-Kivu, Kasaï, Tshopo, Autre"),
        ("radio", "Votre entité", "Une réponse parmi quelques options.", False,
         "Ministère, Agence ou établissement public, Province, Commune"),
        ("date", "Date souhaitée pour un échange", "Une date.", False, ""),
    ]


# Champs RichTextField d'une page : du HTML brut, pas un objet RichText — la
# revision de la page est serialisee en JSON, et RichText ne l'est pas.
INTRO_FORMULAIRE = (
    "<p>Voici les types de champs qu’un formulaire peut contenir. Les réponses se "
    "consultent dans le back-office, et une notification peut être envoyée par "
    "courriel à chaque envoi. Ce formulaire de démonstration n’envoie rien.</p>"
)
MERCI_FORMULAIRE = ("<p>Merci ! Ceci est une démonstration : votre réponse est enregistrée dans le "
                    "back-office, personne ne vous recontactera.</p>")
