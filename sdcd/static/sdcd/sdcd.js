/*! Système de design RDC — comportements minimaux.
    L'essentiel du système est en CSS pur : les accordéons, la transcription et
    le pied de page reposent sur <details>, natif et accessible sans script.
    Ne subsiste ici que la bascule de thème. */
(function () {
  "use strict";

  var CLE = "sdcd-theme";
  var racine = document.documentElement;

  /* Une transition CSS ne réévalue pas une valeur issue d'un var() quand le
     jeton change : l'élément garde la couleur résolue avant la bascule. On
     neutralise donc les transitions le temps du basculement. */
  function appliquer(mode) {
    var sombre =
      mode === "sombre" ||
      (mode === "systeme" &&
        window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: dark)").matches);
    racine.classList.add("sdcd-sans-transition");
    racine.setAttribute("data-theme", sombre ? "dark" : "light");
    var rendu = false;
    function rendre() {
      if (rendu) return;
      rendu = true;
      racine.classList.remove("sdcd-sans-transition");
    }
    // Repli en setTimeout : requestAnimationFrame ne se déclenche pas dans un
    // onglet en arrière-plan, ce qui figerait les transitions.
    requestAnimationFrame(function () { requestAnimationFrame(rendre); });
    setTimeout(rendre, 120);
  }

  try {
    appliquer(localStorage.getItem(CLE) || "systeme");
  } catch (e) {
    appliquer("systeme");
  }

  document.addEventListener("change", function (e) {
    var cible = e.target;
    if (!cible || cible.name !== "sdcd-theme") return;
    appliquer(cible.value);
    try { localStorage.setItem(CLE, cible.value); } catch (err) {}
  });
})();
