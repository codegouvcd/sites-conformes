/*! Système de design RDC (SDCD) — comportements.
 *
 *  Rend le système utilisable hors React : Django, FastAPI, WordPress, HTML pur.
 *  Le CSS du SDCD exprime ses états par attributs ARIA ; ce fichier est ce qui
 *  les pose. Sans lui, les composants s'affichent mais ne réagissent pas.
 *
 *  Principes
 *  ---------
 *  - Aucune dépendance, aucun build. Un `<script src>` suffit.
 *  - Délégation d'événements sur `document` : le contenu injecté après
 *    chargement fonctionne sans réinitialisation.
 *  - Amélioration progressive : ce qui peut être natif l'est (`<details>`,
 *    `<dialog>`), et ce fichier ne fait que compléter.
 *  - L'état vit dans le DOM, pas dans une variable : `aria-expanded`,
 *    `aria-selected`, `aria-pressed`… sont à la fois le style et l'accessibilité.
 *
 *  Licence : MIT (LICENSE). Marque d'État réservée — voir TRADEMARK.md.
 */
(function () {
  "use strict";

  var RACINE = document.documentElement;

  // ---------------------------------------------------------------- outils

  function surClic(selecteur, action) {
    document.addEventListener("click", function (e) {
      var cible = e.target.closest(selecteur);
      if (cible) action(cible, e);
    });
  }

  function estVrai(el, attribut) {
    var v = el.getAttribute(attribut);
    return v === "true" || v === "page";
  }

  /** Bascule un attribut ARIA booléen et renvoie le nouvel état. */
  function basculer(el, attribut) {
    var neuf = !estVrai(el, attribut);
    el.setAttribute(attribut, neuf ? "true" : "false");
    return neuf;
  }

  /** Sélection exclusive : un seul élément marqué dans le groupe. */
  function exclusif(el, groupe, attribut, valeurActive) {
    var conteneur = el.closest(groupe);
    if (!conteneur) return;
    var freres = conteneur.querySelectorAll("[" + attribut + "]");
    for (var i = 0; i < freres.length; i++) {
      if (conteneur.contains(freres[i])) {
        freres[i].setAttribute(attribut, freres[i] === el ? (valeurActive || "true") : "false");
      }
    }
  }

  function afficher(id, visible) {
    var el = id && document.getElementById(id);
    if (el) el.hidden = !visible;
  }

  // ---------------------------------------------------------------- thème
  //
  // Une transition CSS ne réévalue pas une valeur issue d'un var() quand le
  // jeton change : l'élément garde la couleur résolue avant la bascule. On
  // neutralise donc les transitions le temps du basculement.

  var CLE_THEME = "sdcd-theme";

  function appliquerTheme(mode) {
    var sombre =
      mode === "sombre" ||
      (mode === "systeme" &&
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches);
    RACINE.classList.add("sdcd-sans-transition");
    RACINE.setAttribute("data-theme", sombre ? "dark" : "light");
    var rendu = false;
    function rendre() {
      if (rendu) return;
      rendu = true;
      RACINE.classList.remove("sdcd-sans-transition");
    }
    // Double rAF pour laisser le style se recalculer ; repli en setTimeout car
    // requestAnimationFrame ne se déclenche pas dans un onglet en arrière-plan,
    // ce qui laisserait les transitions désactivées indéfiniment.
    requestAnimationFrame(function () { requestAnimationFrame(rendre); });
    setTimeout(rendre, 120);
  }

  try {
    appliquerTheme(localStorage.getItem(CLE_THEME) || "systeme");
  } catch (e) {
    appliquerTheme("systeme");
  }

  surClic(".sdcd-display__option", function (el) {
    // `el` est le <label> : il n'a pas de propriete `value`, si bien que le mode
    // retombait toujours sur « systeme » et le choix du visiteur restait sans
    // effet. On lit d'abord l'attribut explicite, puis le bouton radio contenu,
    // qui est le balisage naturel d'un choix exclusif.
    var champ = el.querySelector("input[type=radio]");
    var mode = el.getAttribute("data-sdcd-theme") || (champ && champ.value) || el.value || "systeme";
    exclusif(el, ".sdcd-display", "aria-checked");
    appliquerTheme(mode);
    try { localStorage.setItem(CLE_THEME, mode); } catch (err) {}
  });

  // ---------------------------------------------------------------- fermeture
  //
  // Un `onclick` en ligne serait plus court, mais il exige `unsafe-inline`
  // dans la politique de sécurité de contenu — c'est-à-dire renoncer à la
  // protection principale contre l'injection de script. Les composants
  // déclarent donc leur intention par un attribut de données, et la fermeture
  // est traitée ici.

  surClic("[data-sdcd-fermer-parent]", function (el) {
    var cible = el.closest(el.getAttribute("data-sdcd-fermer-parent"));
    if (cible) cible.remove();
  });

  // ---------------------------------------------------------------- interrupteur

  surClic(".sdcd-toggle__piste", function (el) {
    var actif = basculer(el, "aria-checked");
    el.dispatchEvent(new CustomEvent("sdcd:bascule", { bubbles: true, detail: { actif: actif } }));
  });

  // ---------------------------------------------------------------- segmenté

  surClic(".sdcd-segmented__option", function (el) {
    exclusif(el, ".sdcd-segmented", "aria-checked");
    var cible = el.getAttribute("aria-controls");
    if (cible) {
      var groupe = el.closest(".sdcd-segmented");
      var options = groupe ? groupe.querySelectorAll("[aria-controls]") : [];
      for (var i = 0; i < options.length; i++) {
        afficher(options[i].getAttribute("aria-controls"), options[i] === el);
      }
    }
  });

  // ---------------------------------------------------------------- étiquettes

  surClic(".sdcd-tag[aria-pressed]", function (el) {
    basculer(el, "aria-pressed");
  });

  // Créneaux et jours de calendrier : sélection unique dans le groupe.
  surClic(".sdcd-creneau", function (el) {
    exclusif(el, ".sdcd-rdv__jours, .sdcd-rdv__horaires, .sdcd-grid", "aria-pressed");
  });
  surClic(".sdcd-calendar__jour", function (el) {
    exclusif(el, ".sdcd-calendar__grille", "aria-pressed");
  });

  // Bascules simples : outils de tableau, graphique/tableau.
  surClic(".sdcd-chart__bascule, .sdcd-datatable__outil[aria-pressed]", function (el) {
    var actif = basculer(el, "aria-pressed");
    var cible = el.getAttribute("aria-controls");
    if (cible) afficher(cible, actif);
  });

  // ---------------------------------------------------------------- accordéon
  //
  // Deux écritures acceptées : <details> natif — rien à faire — ou un bouton
  // portant aria-expanded et aria-controls.

  // ------------------------------------------------- menu de l'en-tête
  //
  // Header.jsx tient cet état dans React ; les intégrations en HTML simple
  // — Django, WordPress, FastAPI — n'avaient rien, si bien que le menu ne
  // s'ouvrait pas du tout sur mobile. L'état vit dans `aria-expanded`, et la
  // cible est masquée par l'attribut `hidden` plutôt que par une classe :
  // un lecteur d'écran ne l'annonce alors pas non plus.
  // Repli d'un menu lateral. Meme mecanique que le menu d'en-tete : le bouton
  // porte aria-expanded et aria-controls, la cible est masquee par `hidden`.
  // Sans ce comportement, une integration en HTML simple se retrouvait avec un
  // bouton inerte — le JavaScript du DSFR le pilotait, il n'a pas ete remplace.
  // Depliage du fil d'Ariane sur petit ecran. Troisieme bouton de cette famille
  // — apres le menu d'en-tete et le menu lateral — a porter aria-expanded et
  // aria-controls sans que rien ne les pilote. Le JavaScript du DSFR s'en
  // chargeait ; son retrait a laisse trois commandes inertes.
  surClic(".sdcd-breadcrumb__bouton[aria-controls]", function (el) {
    var ouvert = basculer(el, "aria-expanded");
    afficher(el.getAttribute("aria-controls"), ouvert);
  });

  surClic(".sdcd-sidemenu__entete[aria-controls]", function (el) {
    var ouvert = basculer(el, "aria-expanded");
    afficher(el.getAttribute("aria-controls"), ouvert);
  });

  surClic(".sdcd-header__menu[aria-controls]", function (el) {
    var ouvert = basculer(el, "aria-expanded");
    afficher(el.getAttribute("aria-controls"), ouvert);
    var icone = el.querySelector("i");
    if (icone) icone.className = ouvert ? "ri-close-line" : "ri-menu-line";
  });

  surClic(".sdcd-accordion__entete[aria-expanded]", function (el) {
    var ouvert = basculer(el, "aria-expanded");
    afficher(el.getAttribute("aria-controls"), ouvert);
  });

  // ---------------------------------------------------------------- onglets

  function activerOnglet(el) {
    var liste = el.closest(".sdcd-tabs__liste, .sdcd-tabs, .sdcd-tabnav");
    if (!liste) return;
    var onglets = liste.querySelectorAll("[role='tab'], .sdcd-tabs__onglet, .sdcd-tabnav__lien");
    for (var i = 0; i < onglets.length; i++) {
      var actif = onglets[i] === el;
      if (onglets[i].hasAttribute("aria-selected")) {
        onglets[i].setAttribute("aria-selected", actif ? "true" : "false");
      }
      if (onglets[i].classList.contains("sdcd-tabnav__lien")) {
        if (actif) onglets[i].setAttribute("aria-current", "page");
        else onglets[i].removeAttribute("aria-current");
      }
      onglets[i].setAttribute("tabindex", actif ? "0" : "-1");
      afficher(onglets[i].getAttribute("aria-controls"), actif);
    }
    el.focus();
  }

  surClic(".sdcd-tabs__onglet, .sdcd-tabnav__lien[aria-controls]", function (el, e) {
    e.preventDefault();
    activerOnglet(el);
  });

  // Flèches gauche/droite entre onglets — exigence clavier du motif ARIA.
  document.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
    var el = e.target.closest(".sdcd-tabs__onglet, .sdcd-tabnav__lien[aria-controls]");
    if (!el) return;
    var liste = el.closest(".sdcd-tabs__liste, .sdcd-tabs, .sdcd-tabnav");
    if (!liste) return;
    var onglets = Array.prototype.slice.call(
      liste.querySelectorAll(".sdcd-tabs__onglet, .sdcd-tabnav__lien[aria-controls]"));
    var i = onglets.indexOf(el);
    var suivant = onglets[(i + (e.key === "ArrowRight" ? 1 : -1) + onglets.length) % onglets.length];
    if (suivant) { e.preventDefault(); activerOnglet(suivant); }
  });

  // ---------------------------------------------------------------- carrousel

  function allerA(carousel, index) {
    var diapos = carousel.querySelectorAll(".sdcd-carousel__diapo");
    var puces = carousel.querySelectorAll(".sdcd-carousel__puce");
    if (!diapos.length) return;
    var n = (index + diapos.length) % diapos.length;
    var piste = carousel.querySelector(".sdcd-carousel__piste");
    if (piste) piste.style.setProperty("--sdcd-carousel-index", n);
    for (var i = 0; i < puces.length; i++) {
      puces[i].setAttribute("aria-current", i === n ? "true" : "false");
    }
    var compteur = carousel.querySelector(".sdcd-carousel__compteur");
    if (compteur) compteur.textContent = (n + 1) + " / " + diapos.length;
    carousel.setAttribute("data-sdcd-index", n);
  }

  function indexCourant(carousel) {
    return parseInt(carousel.getAttribute("data-sdcd-index") || "0", 10);
  }

  surClic(".sdcd-carousel__fleche", function (el) {
    var c = el.closest(".sdcd-carousel");
    if (!c) return;
    allerA(c, indexCourant(c) + (el.classList.contains("sdcd-carousel__fleche--suivant") ? 1 : -1));
  });

  surClic(".sdcd-carousel__puce", function (el) {
    var c = el.closest(".sdcd-carousel");
    if (!c) return;
    var puces = Array.prototype.slice.call(c.querySelectorAll(".sdcd-carousel__puce"));
    allerA(c, puces.indexOf(el));
  });

  // ---------------------------------------------------------------- menus déroulants
  //
  // Menu de langue, menu de compte, listes déroulantes : même motif —
  // un déclencheur avec aria-expanded, un panneau avec aria-controls.

  function fermerMenus(sauf) {
    var ouverts = document.querySelectorAll("[aria-expanded='true'][aria-controls]");
    for (var i = 0; i < ouverts.length; i++) {
      if (ouverts[i] === sauf) continue;
      if (ouverts[i].closest(".sdcd-accordion")) continue; // l'accordéon reste ouvert
      ouverts[i].setAttribute("aria-expanded", "false");
      afficher(ouverts[i].getAttribute("aria-controls"), false);
    }
  }

  surClic(".sdcd-langmenu__declencheur, .sdcd-dropdown__declencheur, [data-sdcd-menu]", function (el, e) {
    e.preventDefault();
    var ouvert = basculer(el, "aria-expanded");
    fermerMenus(el);
    afficher(el.getAttribute("aria-controls"), ouvert);
  });

  // Un bouton « Fermer » place a l'interieur d'une region depliee nomme celle-ci
  // dans `data-sdcd-replie`. On remet aussi le declencheur — celui dont
  // aria-controls vise la meme region — a aria-expanded="false" : sans cela le
  // bouton annoncerait une region ouverte alors qu'elle vient d'etre fermee, et
  // un second clic ne la rouvrirait pas.
  surClic("[data-sdcd-replie]", function (el) {
    var id = el.getAttribute("data-sdcd-replie");
    if (!id) return;
    afficher(id, false);
    var declencheurs = document.querySelectorAll(
      "[aria-expanded][aria-controls='" + id + "']");
    for (var i = 0; i < declencheurs.length; i++) {
      declencheurs[i].setAttribute("aria-expanded", "false");
    }
  });

  surClic(".sdcd-langmenu__option", function (el) {
    exclusif(el, ".sdcd-langmenu__liste, .sdcd-langmenu", "aria-current");
    fermerMenus();
  });

  // Clic hors menu et touche Échap referment.
  document.addEventListener("click", function (e) {
    if (!e.target.closest("[aria-expanded][aria-controls], .sdcd-langmenu, .sdcd-dropdown")) {
      fermerMenus();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    fermerMenus();
    var tiroir = document.querySelector(".sdcd-aside[data-ouvert='true']");
    if (tiroir) fermerTiroir();
  });

  // ---------------------------------------------------------------- tiroir latéral
  //
  // Sous 900 px, `.sdcd-aside` devient un tiroir hors-écran piloté par
  // data-ouvert, avec un voile `.sdcd-voile`.

  function ouvrirTiroir() {
    var aside = document.querySelector(".sdcd-aside");
    var voile = document.querySelector(".sdcd-voile");
    if (aside) aside.setAttribute("data-ouvert", "true");
    if (voile) voile.setAttribute("data-ouvert", "true");
    var declencheur = document.querySelector("[data-sdcd-tiroir]");
    if (declencheur) declencheur.setAttribute("aria-expanded", "true");
    if (aside) {
      var premier = aside.querySelector("a, button");
      if (premier) premier.focus();
    }
  }

  function fermerTiroir() {
    var aside = document.querySelector(".sdcd-aside");
    var voile = document.querySelector(".sdcd-voile");
    if (aside) aside.removeAttribute("data-ouvert");
    if (voile) voile.removeAttribute("data-ouvert");
    var declencheur = document.querySelector("[data-sdcd-tiroir]");
    if (declencheur) {
      declencheur.setAttribute("aria-expanded", "false");
      declencheur.focus();
    }
  }

  surClic("[data-sdcd-tiroir]", function (el) {
    if (estVrai(el, "aria-expanded")) fermerTiroir();
    else ouvrirTiroir();
  });

  surClic(".sdcd-voile", fermerTiroir);

  // ---------------------------------------------------------------- modale
  //
  // S'appuie sur <dialog> : la gestion du focus, de la touche Échap et du
  // voile est native. On ne fournit que l'ouverture et la fermeture.

  surClic("[data-sdcd-ouvre]", function (el) {
    var d = document.getElementById(el.getAttribute("data-sdcd-ouvre"));
    if (!d) return;
    if (typeof d.showModal === "function") d.showModal();
    else d.setAttribute("open", "");
  });

  surClic("[data-sdcd-ferme], .sdcd-modal__fermer", function (el) {
    var d = el.closest("dialog") ||
            document.getElementById(el.getAttribute("data-sdcd-ferme") || "");
    if (!d) return;
    if (typeof d.close === "function") d.close();
    else d.removeAttribute("open");
  });

  // Clic sur le voile d'une <dialog> : ferme si le clic tombe hors du contenu.
  document.addEventListener("click", function (e) {
    var d = e.target;
    if (d.tagName !== "DIALOG") return;
    var r = d.getBoundingClientRect();
    var dehors = e.clientX < r.left || e.clientX > r.right ||
                 e.clientY < r.top || e.clientY > r.bottom;
    if (dehors && typeof d.close === "function") d.close();
  });

  // ---------------------------------------------------------------- tableau défilant
  //
  // `.sdcd-scroll-x[data-discret]` masque sa barre et signale la suite par un
  // dégradé de bord ; data-debut / data-fin indiquent où l'on se trouve.

  function majDefilement(el) {
    var aDebut = el.scrollLeft <= 1;
    var aFin = el.scrollLeft + el.clientWidth >= el.scrollWidth - 1;
    if (aDebut) el.setAttribute("data-debut", "true"); else el.removeAttribute("data-debut");
    if (aFin) el.setAttribute("data-fin", "true"); else el.removeAttribute("data-fin");
  }

  function initDefilement() {
    var zones = document.querySelectorAll(".sdcd-scroll-x[data-discret]");
    for (var i = 0; i < zones.length; i++) {
      majDefilement(zones[i]);
      zones[i].addEventListener("scroll", function () { majDefilement(this); }, { passive: true });
    }
  }

  // ---------------------------------------------------------------- amorçage

  function initialiser() {
    initDefilement();
    // Carrousels : poser l'index initial et le compteur.
    var carousels = document.querySelectorAll(".sdcd-carousel");
    for (var i = 0; i < carousels.length; i++) {
      if (!carousels[i].hasAttribute("data-sdcd-index")) allerA(carousels[i], 0);
    }
    RACINE.setAttribute("data-sdcd-js", "actif");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialiser);
  } else {
    initialiser();
  }

  // Exposé pour les intégrations qui insèrent du contenu à la volée.
  window.SDCD = {
    version: "0.6.0",
    theme: appliquerTheme,
    carousel: allerA,
    tiroir: { ouvrir: ouvrirTiroir, fermer: fermerTiroir },
    rafraichir: initialiser
  };
})();
