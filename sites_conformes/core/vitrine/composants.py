"""Les pages de composants : chaque bloc du CMS dans ses variantes, avec un
contenu qui parle des services publics congolais.

Ces pages remplacent les copies des modeles amont, dont le contenu etait
generique (« Argument #1 », illustrations d'un autre site). Chacune ouvre par
ce que le bloc fait et ou le trouver dans le back-office, puis le montre.
"""

from .outils import (
    accordeons,
    alerte,
    ancre,
    badges,
    bouton,
    boutons,
    carte,
    carte_horizontale,
    citation,
    colonnes,
    encadre,
    etapier,
    etiquettes,
    fiche_contact,
    fond,
    fond_menu_lateral,
    grille,
    hero_image_texte,
    image_centree,
    image_texte,
    lien_simple,
    mise_en_avant,
    onglets,
    paragraphe,
    rt,
    separateur,
    texte_appel,
    tuile,
)


def _intro(html, bloc, groupe):
    return paragraphe(
        f"<p class=\"sdcd-texte-lead\">{html}</p>"
        f"<p>Dans le back-office, ce bloc s’appelle <strong>{bloc}</strong>, "
        f"dans le groupe « {groupe} » de l’éditeur de contenu.</p>"
    )


# ------------------------------------------------------------------ tuiles
def tuiles(images, pages):
    return [
        _intro("La tuile met en avant une entrée : un service, une rubrique, un guide. "
               "Elle porte un titre, un court texte, un pictogramme, et devient cliquable "
               "en entier dès qu’un lien lui est donné.", "Tuile", "Composants"),
        paragraphe("<h2>Trois entrées vers les services</h2>"),
        grille([
            ("tile", tuile("Acte de naissance", "Déclarer une naissance et obtenir l’acte, en ligne ou au guichet.",
                           page=pages["catalogue-de-services"], image=images["picto-conformite"])),
            ("tile", tuile("Passeport biométrique", "Prendre rendez-vous, préparer le dossier, suivre la fabrication.",
                           page=pages["catalogue-de-services"], image=images["picto-securite"])),
            ("tile", tuile("Créer son entreprise", "Le guichet unique, les pièces à fournir, les délais.",
                           page=pages["catalogue-de-services"], image=images["picto-autonomie"])),
        ], largeur="4"),
        paragraphe("<h2>Tuiles petites, avec badge</h2>"
                   "<p>La variante petite convient aux listes longues : un titre, une ligne, un badge d’état.</p>"),
        grille([
            ("tile", tuile("Formation des rédacteurs", "Session en ligne, 12 mars.", page=pages["agenda"],
                           petite=True, badge="Inscriptions ouvertes")),
            ("tile", tuile("Guide de démarrage", "Six étapes pour ouvrir un site.", page=pages["creer-votre-site"],
                           petite=True, badge="Mis à jour", couleur_badge="succes")),
            ("tile", tuile("Audit d’accessibilité", "Premiers résultats publiés.", page=pages["actualites"],
                           petite=True, badge="Nouveau", couleur_badge="chart-2")),
            ("tile", tuile("Questions fréquentes", "Hébergement, domaine, responsabilités.",
                           page=pages["questions-frequentes"], petite=True)),
        ], largeur="3"),
        paragraphe("<h2>Tuile avec texte de détail</h2>"
                   "<p>Le détail, sous la description, précise une date, un format ou une durée.</p>"),
        grille([
            ("tile", tuile("Concertation de Lubumbashi", "Les services de la ville rencontrent les usagers.",
                           page=pages["agenda"], image=images["picto-budget"], detail="Samedi 21 mars, 9 h — Hôtel de ville")),
            ("tile", tuile("Conférence : services publics en ligne", "Retours des premiers ministères équipés.",
                           page=pages["agenda"], image=images["picto-conformite"], detail="Jeudi 2 avril — Kinshasa, en présentiel et en ligne")),
        ], largeur="6"),
    ]


# ------------------------------------------------------------------ cartes
def cartes(images, pages):
    return [
        _intro("La carte présente un contenu daté ou illustré : un article, un événement, un service. "
               "Verticale dans une grille, horizontale seule, elle accepte image, étiquettes, badge, "
               "détail et boutons.", "Carte verticale (dans une grille) ou Carte horizontale", "Composants"),
        paragraphe("<h2>Cartes verticales, sur trois colonnes</h2>"),
        grille([
            ("card", carte("Dorsale nationale : Goma raccordée", "La fibre relie désormais les services de l’État du Nord-Kivu.",
                           page=pages["actualites"], image=images["actualite-numerique"], ratio="sdcd-ratio-16x9",
                           etiquettes=("Numérique", "Infrastructures"))),
            ("card", carte("Kikwit : un site en une semaine", "La ville a ouvert son site avec trois agents formés.",
                           page=pages["actualites"], image=images["actualite-formation"], ratio="sdcd-ratio-16x9",
                           etiquettes=("Collectivités",))),
            ("card", carte("Accessibilité : premiers audits", "Vingt sites contrôlés, les écarts les plus fréquents.",
                           page=pages["actualites"], image=images["actualite-accessibilite"], ratio="sdcd-ratio-16x9",
                           etiquettes=("Accessibilité",))),
        ], largeur="4"),
        paragraphe("<h2>Cartes avec badge, détail et fond gris</h2>"
                   "<p>Le détail du haut porte une icône : une date, un lieu, une durée.</p>"),
        grille([
            ("card", carte("Atelier de prise en main", "Une matinée pour créer ses premières pages.",
                           page=pages["agenda"], image=images["evenement-atelier"], ratio="sdcd-ratio-3x2",
                           badge="Complet", couleur_badge="alerte", detail_haut="Mardi 10 mars, 9 h", icone_haut="ri-calendar-line")),
            ("card", carte("Formation des rédacteurs en ligne", "Quatre séances d’une heure, à distance.",
                           page=pages["agenda"], image=images["evenement-formation"], ratio="sdcd-ratio-3x2",
                           badge="Inscriptions ouvertes", couleur_badge="succes", detail_haut="Du 16 au 19 mars", icone_haut="ri-calendar-line",
                           fond_gris=True)),
        ], largeur="6"),
        paragraphe("<h2>Carte horizontale</h2>"
                   "<p>Seule sur sa ligne, l’image à gauche sur un tiers ou la moitié de la largeur.</p>"),
        carte_horizontale("Passeport biométrique", "Rendez-vous en ligne, dossier complet, retrait sous trois semaines. "
                          "Le service est ouvert dans les capitales provinciales.",
                          page=pages["catalogue-de-services"], image=images["service-passeport"], ratio="sdcd-card--horizontal-tiers",
                          etiquettes=("Identité",), detail_bas="Mis à jour le 3 septembre 2026"),
        carte_horizontale("Déclarer ses impôts", "Les entreprises déclarent en ligne, les particuliers au centre des impôts "
                          "de leur commune.", page=pages["catalogue-de-services"], image=images["service-impots"],
                          ratio="sdcd-card--horizontal-moitie",
                          appel=[bouton("Commencer la déclaration", page=pages["formulaire-de-demonstration"]),
                                 bouton("Lire la notice", page=pages["creer-votre-site"], type_="sdcd-button sdcd-button--secondaire")]),
    ]


# -------------------------------------------------------------- accordeons
def accordeons_page(images, pages):
    return [
        _intro("L’accordéon replie un contenu long derrière son titre : questions fréquentes, "
               "pièces à fournir, conditions. Le lecteur ouvre ce qui le concerne.", "Accordéons", "Composants"),
        accordeons("Ouvrir un site pour son administration", [
            ("Qui peut demander un site ?", "<p>Tout ministère, service, agence ou collectivité de la République. "
                                             "La demande est portée par le responsable de la communication ou le "
                                             "secrétaire général.</p>"),
            ("Combien de temps faut-il ?", "<p>Le site est ouvert en moins d’une journée. Compter une semaine pour "
                                           "rédiger les premières pages et former les rédacteurs.</p>"),
            ("Quel est le coût ?", "<p>Aucun. L’hébergement, le nom de domaine en <code>.gouv.cd</code> et les mises "
                                   "à jour sont pris en charge par la plateforme.</p>"),
            ("Que devient l’ancien site ?", "<p>Ses contenus sont repris page par page, ses adresses redirigées. "
                                            "L’ancien site est fermé quand le nouveau est complet.</p>"),
        ]),
        separateur(),
        accordeons("Pièces à fournir pour un acte de naissance", [
            ("Naissance déclarée dans les 90 jours", "<ul><li>l’attestation de naissance de la maternité ;</li>"
                                                     "<li>la carte d’électeur ou le passeport d’un parent ;</li>"
                                                     "<li>l’acte de mariage, s’il y a lieu.</li></ul>"),
            ("Déclaration tardive", "<p>Au-delà de 90 jours, un jugement supplétif du tribunal de paix est "
                                    "nécessaire. Le greffe indique les pièces et les frais.</p>"),
            ("Retrait de l’acte", "<p>Au guichet de l’état civil de la commune, sur présentation du récépissé. "
                                  "Un tiers peut retirer l’acte avec une procuration.</p>"),
        ], niveau="h2"),
    ]


# ---------------------------------------------------------------- etapiers
def etapiers(images, pages):
    return [
        _intro("L’étapier dit où l’on en est dans une démarche et ce qu’il reste à faire : "
               "un compte d’étapes, une jauge, l’étape suivante, puis la liste des étapes avec leur état.",
               "Étapier", "Composants"),
        paragraphe("<h2>Au début d’une démarche</h2>"),
        etapier("Déclarer une naissance", 3, 1, [
            ("Déclarer", "En ligne ou au guichet, avec l’attestation de la maternité."),
            ("Vérifier", "L’officier d’état civil contrôle le dossier sous cinq jours."),
            ("Retirer", "L’acte est remis au guichet, sur récépissé."),
        ], niveau="h3"),
        paragraphe("<h2>En cours de démarche</h2>"),
        etapier("Obtenir un passeport biométrique", 5, 3, [
            ("Prendre rendez-vous", "En ligne, dans le centre de votre choix."),
            ("Déposer le dossier", "Acte de naissance, carte d’électeur, photo, quittance."),
            ("Enrôlement", "Empreintes et photo pris sur place, en dix minutes."),
            ("Fabrication", "Le passeport est produit à Kinshasa sous trois semaines."),
            ("Retrait", "Au centre du dépôt, sur présentation du récépissé."),
        ], niveau="h3"),
        paragraphe("<h2>Démarche terminée</h2>"),
        etapier("Créer son entreprise", 4, 4, [
            ("Vérifier la dénomination", "Le nom choisi ne doit pas déjà exister."),
            ("Déposer les statuts", "Au guichet unique de création d’entreprise."),
            ("Obtenir le RCCM et l’identification nationale", "Délivrés ensemble, sous trois jours."),
            ("Recevoir le numéro d’impôt", "Attribué automatiquement à la création."),
        ], niveau="h3"),
    ]


# ------------------------------------------------ en-tetes et bandeaux
def en_tetes(images, pages):
    hero = [
        hero_image_texte(
            "Un en-tête avec image et texte",
            "<p>Cette page s’ouvre sur l’en-tête « image et texte » : le titre et l’accroche à gauche, "
            "une image à droite, jusqu’à deux boutons. Deux autres en-têtes existent : le bandeau large "
            "et l’image de fond, que montrent la page d’atterrissage et le site vitrine.</p>",
            [bouton("Voir la page d’atterrissage", page=pages["page-atterrissage"], icone="ri-arrow-right-line", cote="droite"),
             bouton("Voir le site vitrine", page=pages["site-vitrine"], type_="sdcd-button sdcd-button--secondaire")],
            images["hero-vitrine"],
        )
    ]
    corps = [
        _intro("Les en-têtes se règlent dans l’onglet « En-tête » de la page ; les bandeaux d’appel "
               "à action sont des blocs « Fond pleine largeur » et « Texte et appel à action » "
               "placés dans le corps.", "Fond pleine largeur", "Structure de page"),
        fond([
            ("text", rt("<h2>Un bandeau sur fond bleu</h2>"
                        "<p>Le fond pleine largeur sort du conteneur : il rythme une page longue et isole "
                        "un message. Il accepte n’importe quel bloc, ici un texte et deux boutons.</p>")),
            ("buttons_list", {"buttons": [("button", bouton("Ouvrir mon site", page=pages["contact"])),
                                          ("button", bouton("Lire le guide", page=pages["creer-votre-site"],
                                                            type_="sdcd-button sdcd-button--secondaire"))], "position": ""}),
        ], couleur="bleu"),
        fond([
            ("text", rt("<h2>Un bandeau sur image</h2>"
                        "<p>La même structure, avec une image de fond. Le texte reste lisible grâce au "
                        "voile que le système applique.</p>")),
        ], couleur="bleu-soutenu", image=images["hero-accueil"]),
        paragraphe("<h2>Texte et appel à action</h2>"
                   "<p>Le bloc le plus simple pour finir une page : une phrase et un bouton.</p>"),
        texte_appel("<p>Votre administration n’a pas encore de site ? La demande prend cinq minutes.</p>",
                    [bouton("Demander un site", page=pages["contact"], icone="ri-send-plane-line", cote="gauche")]),
        fond([
            ("text", rt("<h2>Un bandeau gris soutenu</h2>"
                        "<p>Pour un pied de section, une citation, un chiffre clé.</p>")),
        ], couleur="gris-soutenu", haut=4, bas=4),
    ]
    return hero, corps


# ------------------------------------------- blocs simples de textes et images
def blocs_simples(images, pages):
    return [
        _intro("Le texte riche, l’image, l’image avec texte, la citation, les boutons et le lien : "
               "les blocs de base, ceux de la plupart des pages.", "Texte riche", "Blocs de base"),
        paragraphe(
            "<h2>Texte riche</h2>"
            "<p>Le texte riche accepte les titres, les paragraphes, les listes, les liens, le gras et "
            "l’italique. Un titre de niveau 2 ouvre une section ; un niveau 3, une sous-section.</p>"
            "<h3>Une liste</h3>"
            "<ul><li>Chaque site est hébergé en République Démocratique du Congo.</li>"
            "<li>Le nom de domaine se termine par <code>.gouv.cd</code>.</li>"
            "<li>Les contenus sont sous licence ouverte de l’État congolais.</li></ul>"
            "<h3>Une liste numérotée</h3>"
            "<ol><li>Demander l’ouverture du site.</li><li>Former deux rédacteurs.</li><li>Publier.</li></ol>"
            "<p>Un <a href=\"/documentation/\">lien interne</a>, un <a href=\"https://www.w3.org/WAI/standards-guidelines/wcag/\">"
            "lien externe</a>, un <a href=\"mailto:contact@example.cd\">lien courriel</a>.</p>"
        ),
        paragraphe("<h2>Image centrée</h2>"),
        image_centree(images["illustration-redaction"], "Une rédactrice prépare une page depuis le back-office.",
                      alt="Composition : une feuille et un crayon", largeur="sdcd-media--sm"),
        paragraphe("<h2>Image et texte</h2><p>L’image à gauche ou à droite, sur un tiers, un quart ou la moitié.</p>"),
        image_texte(images["illustration-securite"],
                    "<h3>Un hébergement souverain</h3><p>Les sites sont servis depuis Kinshasa, sauvegardés "
                    "chaque nuit, et mis à jour sans intervention des administrations.</p>",
                    cote="left", largeur="4"),
        image_texte(images["illustration-blocs"],
                    "<h3>Des blocs, pas du code</h3><p>Chaque page s’assemble bloc par bloc. Le rédacteur "
                    "choisit, remplit, publie : la mise en page est celle du système de design.</p>",
                    cote="right", largeur="4"),
        paragraphe("<h2>Citation</h2>"),
        citation("Nous avons publié le site du ministère en trois jours, avec deux agents qui n’avaient "
                 "jamais touché à un outil de publication.",
                 "Grâce Mbuyi", "Chargée de communication, ministère du Numérique", image=images["portrait-agente"]),
        paragraphe("<h2>Boutons</h2><p>Primaire, secondaire, tertiaire ; avec ou sans icône ; alignés à gauche, au centre ou à droite.</p>"),
        boutons(bouton("Bouton primaire", page=pages["accueil"]),
                bouton("Secondaire", page=pages["accueil"], type_="sdcd-button sdcd-button--secondaire"),
                bouton("Tertiaire", page=pages["accueil"], type_="sdcd-button sdcd-button--tertiaire"),
                bouton("Avec icône", page=pages["accueil"], icone="ri-download-line", cote="gauche")),
        boutons(bouton("Centré", page=pages["accueil"]),
                bouton("Et secondaire", page=pages["accueil"], type_="sdcd-button sdcd-button--secondaire"),
                position="sdcd-boutons--centre"),
        paragraphe("<h2>Lien simple</h2>"),
        lien_simple("Toute la documentation", page=pages["documentation"], icone="ri-arrow-right-line sdcd-lien--icone-droite"),
        lien_simple("Le système de design, en grand", page=pages["systeme-de-design"], taille="sdcd-lien--lg"),
        separateur(),
        paragraphe("<p>Le séparateur, juste au-dessus, marque la fin d’une section sans titre.</p>"),
    ]


# --------------------------------------------- options de mise en valeur
def mise_en_valeur(images, pages):
    return [
        _intro("Alerte, encadré, mise en avant, badges et étiquettes : les blocs qui font ressortir "
               "une information sans casser la lecture.", "Message d’alerte, Encadré, Mise en avant", "Composants"),
        paragraphe("<h2>Messages d’alerte</h2><p>Quatre niveaux, chacun avec son icône et sa couleur.</p>"),
        alerte("Information", "Les guichets de l’état civil sont ouverts du lundi au vendredi, de 8 h à 15 h.", "info"),
        alerte("Demande enregistrée", "Votre déclaration a été reçue. Vous recevrez un SMS quand l’acte sera prêt.", "success"),
        alerte("Attention aux intermédiaires", "Aucun site officiel ne demande de paiement par téléphone portable pour un acte.", "warning"),
        alerte("Service indisponible", "Le service de prise de rendez-vous est interrompu jusqu’à lundi 8 h.", "error"),
        paragraphe("<h2>Encadrés</h2><p>Un titre, une icône, un texte, parfois un bouton ; la couleur vient de la palette d’illustration.</p>"),
        encadre("Besoin d’aide pour remplir le formulaire ?",
                "<p>Un agent vous reçoit sans rendez-vous à la maison communale, du lundi au vendredi.</p>",
                icone="ri-customer-service-2-line", couleur="chart-1",
                bouton_=bouton("Trouver la maison communale", page=pages["contact"])),
        encadre("Le saviez-vous ?",
                "<p>La déclaration de naissance est gratuite pendant 90 jours. Passé ce délai, un jugement "
                "supplétif est nécessaire.</p>", icone="ri-lightbulb-line", couleur="chart-3"),
        paragraphe("<h2>Mise en avant</h2><p>Un filet de couleur à gauche, en trois tailles.</p>"),
        mise_en_avant("<p>Tout site de l’État congolais doit être lisible au téléphone : c’est ainsi que "
                      "neuf usagers sur dix le consulteront.</p>", couleur="chart-1", taille="sdcd-texte-lg"),
        mise_en_avant("<p>Les contenus publiés relèvent de la responsabilité de chaque administration.</p>",
                      couleur="chart-2"),
        mise_en_avant("<p>Le code source du CMS est libre, sous licence AGPL-3.0.</p>",
                      couleur="chart-4", taille="sdcd-texte-sm"),
        paragraphe("<h2>Badges</h2><p>Un état, en couleurs du système ou d’illustration.</p>"),
        badges("Succès", couleur="succes"),
        badges("Information", "Nouveau", couleur="info"),
        badges("Attention", couleur="alerte"),
        badges("Erreur", couleur="erreur"),
        badges("Numérique", "Collectivités", "Accessibilité", couleur="chart-2"),
        paragraphe("<h2>Étiquettes</h2><p>Une thématique, un mot-clé ; cliquables quand elles portent un lien.</p>"),
        etiquettes("État civil", "Identité", "Entreprises", "Impôts", couleur="chart-1"),
        etiquettes("Kinshasa", "Lubumbashi", "Goma", "Kikwit", couleur="chart-3"),
    ]


# --------------------------------------------------------- grilles d'elements
def grilles(images, pages):
    return [
        _intro("La grille range des tuiles, des cartes ou des colonnes libres sur deux, trois ou quatre "
               "colonnes ; elle s’aligne à gauche, au centre ou à droite.", "Grille d’éléments", "Structure de page"),
        paragraphe("<h2>Quatre colonnes de tuiles</h2>"),
        grille([
            ("tile", tuile("État civil", "Naissances, mariages, décès.", page=pages["catalogue-de-services"], image=images["picto-conformite"], petite=True)),
            ("tile", tuile("Identité", "Passeport, carte d’électeur.", page=pages["catalogue-de-services"], image=images["picto-securite"], petite=True)),
            ("tile", tuile("Entreprises", "Création, registre, licences.", page=pages["catalogue-de-services"], image=images["picto-autonomie"], petite=True)),
            ("tile", tuile("Impôts", "Déclarer, payer, contester.", page=pages["catalogue-de-services"], image=images["picto-budget"], petite=True)),
        ], largeur="3"),
        paragraphe("<h2>Trois colonnes de cartes</h2>"),
        grille([
            ("card", carte("Atelier de prise en main", "Une matinée pour créer ses premières pages.", page=pages["agenda"],
                           image=images["evenement-atelier"], ratio="sdcd-ratio-3x2", detail_haut="10 mars", icone_haut="ri-calendar-line")),
            ("card", carte("Conférence", "Les services publics en ligne : premiers retours.", page=pages["agenda"],
                           image=images["evenement-conference"], ratio="sdcd-ratio-3x2", detail_haut="2 avril", icone_haut="ri-calendar-line")),
            ("card", carte("Concertation de Lubumbashi", "Les services de la ville rencontrent les usagers.", page=pages["agenda"],
                           image=images["evenement-concertation"], ratio="sdcd-ratio-3x2", detail_haut="21 mars", icone_haut="ri-calendar-line")),
        ], largeur="4"),
        paragraphe("<h2>Colonnes réglables</h2><p>Le bloc « Colonnes multiples » reçoit des colonnes de largeur choisie, ici deux fois cinq douzièmes.</p>"),
        colonnes("Qui fait quoi", [
            ("5", [("text", rt("<h3>Ce que la plateforme prend en charge</h3>"
                               "<ul><li>l’hébergement et les sauvegardes ;</li>"
                               "<li>les mises à jour de sécurité ;</li>"
                               "<li>le nom de domaine ;</li>"
                               "<li>le système de design.</li></ul>"))]),
            ("5", [("text", rt("<h3>Ce qui reste à l’administration</h3>"
                               "<ul><li>les contenus et leur exactitude ;</li>"
                               "<li>la réponse aux usagers ;</li>"
                               "<li>la déclaration d’accessibilité ;</li>"
                               "<li>les mentions légales.</li></ul>"))]),
        ], haut=2, bas=2),
        paragraphe("<h2>Colonnes avec titre et fond</h2>"),
        colonnes("Trois chiffres", [
            ("4", [("text", rt("<p class=\"sdcd-display\">64</p><p>sites ouverts depuis janvier</p>"))]),
            ("4", [("text", rt("<p class=\"sdcd-display\">310</p><p>rédacteurs formés</p>"))]),
            ("4", [("text", rt("<p class=\"sdcd-display\">9 / 10</p><p>consultations depuis un téléphone</p>"))]),
        ], couleur="gris"),
    ]


# ------------------------------------------------ page avec menu lateral
def menu_lateral(images, pages):
    contenu = [
        ("anchor", {"anchor_id": "demande"}),
        ("text", rt("<h2>1. La demande</h2>"
                    "<p>Le responsable de la communication écrit au service de la plateforme, avec le nom de "
                    "l’administration, l’adresse souhaitée et deux rédacteurs à former. La réponse arrive sous "
                    "deux jours ouvrés.</p>")),
        ("anchor", {"anchor_id": "ouverture"}),
        ("text", rt("<h2>2. L’ouverture</h2>"
                    "<p>Le site est créé avec son en-tête, son pied de page, ses pages légales et ses menus. Les "
                    "rédacteurs reçoivent leurs accès et une session d’une heure de prise en main.</p>")),
        ("callout", {"title": "Ce que contient un site neuf", "heading_tag": "h3", "icon_class": "ri-checkbox-circle-line",
                     "text": rt("<p>Accueil, mentions légales, déclaration d’accessibilité, contact, plan du site, "
                                "recherche et paramètres d’affichage.</p>"), "color": "chart-1"}),
        ("anchor", {"anchor_id": "redaction"}),
        ("text", rt("<h2>3. La rédaction</h2>"
                    "<p>Les pages s’assemblent avec les blocs de cette rubrique. Chaque page a un résumé, "
                    "une image d’en-tête et un emplacement dans le menu. Une page non publiée reste invisible.</p>")),
        ("anchor", {"anchor_id": "publication"}),
        ("text", rt("<h2>4. La publication</h2>"
                    "<p>Un rédacteur soumet, un responsable publie. Le site est en ligne à l’adresse "
                    "convenue ; l’ancien site est redirigé page par page.</p>")),
        ("anchor", {"anchor_id": "suite"}),
        ("text", rt("<h2>5. Et après</h2>"
                    "<p>Les mises à jour du CMS et du système de design arrivent sans rien faire. Les "
                    "rédacteurs restent responsables des contenus et de leur exactitude.</p>")),
    ]
    return [
        _intro("Le fond pleine largeur avec menu latéral place à gauche l’arbre des pages d’une "
               "rubrique, qui suit la lecture, et à droite le contenu. Il convient aux guides et "
               "aux rubriques profondes.", "Fond pleine largeur avec menu latéral", "Structure de page"),
        fond_menu_lateral(contenu, "Les composants", pages["composants"], couleur="gris"),
    ]


# ------------------------------------- onglets, colonnes et fiches contact
def onglets_contacts(images, pages):
    return [
        _intro("Les onglets rangent plusieurs contenus au même endroit ; la fiche contact présente une "
               "personne ou un service. Ils se combinent en colonnes.", "Onglets, Fiche contact", "Composants"),
        paragraphe("<h2>Onglets</h2>"),
        onglets(
            ("Particuliers", [("text", rt("<h3>Pour les particuliers</h3><p>Acte de naissance, passeport, "
                                          "carte d’électeur, attestation de résidence : les démarches se font "
                                          "en ligne ou au guichet de la commune.</p>")),
                              ("buttons_list", {"buttons": [("button", bouton("Voir les démarches", page=pages["catalogue-de-services"]))], "position": ""})]),
            ("Entreprises", [("text", rt("<h3>Pour les entreprises</h3><p>Création au guichet unique, registre "
                                         "du commerce, identification nationale, déclarations fiscales.</p>")),
                             ("buttons_list", {"buttons": [("button", bouton("Créer son entreprise", page=pages["catalogue-de-services"]))], "position": ""})]),
            ("Administrations", [("text", rt("<h3>Pour les administrations</h3><p>Ouvrir un site, former des "
                                             "rédacteurs, publier des données : la plateforme accompagne chaque étape.</p>")),
                                 ("buttons_list", {"buttons": [("button", bouton("Demander un site", page=pages["contact"]))], "position": ""})]),
        ),
        paragraphe("<h2>Fiches contact</h2>"),
        colonnes("", [
            ("6", [fiche_contact("Grâce Mbuyi", "Chargée de communication", "Ministère du Numérique",
                                 "communication@numerique.gouv.cd — +243 81 000 00 00",
                                 image=images["portrait-agente"], etiquettes_=("Communication",))]),
            ("6", [fiche_contact("Patrick Ilunga", "Responsable des rédacteurs", "Ville de Kikwit",
                                 "redaction@kikwit.gouv.cd",
                                 image=images["portrait-agent"], etiquettes_=("Rédaction", "Formation"))]),
        ], haut=2, bas=2),
        paragraphe("<h2>Colonnes réglables</h2><p>Deux tiers, un tiers : le texte principal et un encadré.</p>"),
        colonnes("", [
            ("8", [("text", rt("<h3>Horaires des guichets</h3>"
                               "<p>Les guichets de l’état civil reçoivent du lundi au vendredi, "
                               "de 8 h à 15 h, sans rendez-vous. Le samedi matin est réservé "
                               "aux retraits d’actes.</p>"))]),
            ("4", [("callout", {"title": "Jours fériés", "heading_tag": "h3", "icon_class": "ri-calendar-close-line",
                                "text": rt("<p>Les guichets sont fermés le 30 juin et le 17 janvier.</p>"),
                                "color": "chart-2"})]),
        ], haut=2, bas=2),
    ]


# ---------------------------------------------------------------- catalogue
# (slug, titre, fonction, vignette, avec_hero)
PAGES = [
    ("tuiles", "Tuiles", tuiles, "actualite-numerique", False),
    ("cartes", "Cartes", cartes, "actualite-accessibilite", False),
    ("accordeons", "Accordéons", accordeons_page, "actualite-formation", False),
    ("etapiers", "Étapiers", etapiers, "service-etat-civil", False),
    ("en-tetes-et-bandeaux", "En-têtes et bandeaux d’appel à action", en_tetes, "hero-vitrine", True),
    ("blocs-simples-de-textes-et-dimages", "Blocs simples de textes et d’images", blocs_simples, "actualite-tribune", False),
    ("options-de-mise-en-valeur-de-textes", "Options de mise en valeur de textes", mise_en_valeur, "evenement-conference", False),
    ("grilles-delements", "Grilles d’éléments", grilles, "evenement-atelier", False),
    ("page-de-contenu-avec-menu-lateral", "Page de contenu avec menu latéral", menu_lateral, "evenement-concertation", False),
    ("onglets-colonnes-et-fiches-contact", "Onglets, colonnes et fiches contact", onglets_contacts, "evenement-formation", False),
]
