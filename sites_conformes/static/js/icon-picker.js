/* Apercu du champ de choix d'icone.
 *
 * Relie chaque champ a son <i> d'apercu et a sa liste de suggestions. Ecrit en
 * delegation pour couvrir les champs que Wagtail ajoute apres le chargement —
 * un bloc de flux insere en cours d'edition, par exemple.
 */
(function () {
  "use strict";

  function relier(champ) {
    var apercu = document.getElementById(champ.id + "-apercu");
    if (!apercu) return;
    var liste = document.getElementById(champ.id + "-liste");
    if (liste) champ.setAttribute("list", liste.id);
    // La classe saisie est appliquee telle quelle : c'est ce que le gabarit du
    // site fera. Une valeur invalide n'affiche rien, ce qui est le retour attendu.
    apercu.className = "icon-picker-widget__apercu " + champ.value.trim();
  }

  function surSaisie(e) {
    var champ = e.target;
    if (champ && champ.closest && champ.closest(".icon-picker-widget")) relier(champ);
  }

  document.addEventListener("input", surSaisie);
  document.addEventListener("change", surSaisie);
  document.addEventListener("DOMContentLoaded", function () {
    var champs = document.querySelectorAll(".icon-picker-widget input[type='text']");
    for (var i = 0; i < champs.length; i++) relier(champs[i]);
  });
})();
