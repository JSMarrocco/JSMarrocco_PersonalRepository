/* Extrait les valeurs produites dans la page Web et par le simulateur
 * et d�clanche l'affichage des valeurs dans la page
*/


/*Code jquery qui affiche un glisseur dans le conteneur ayant
 *l'identifiant #thermostat, qui initalise sa position et ses valeurs
 *par d�faut et qui affiche la valeur s�lectionn�e dans un conteneur
 *ayant l'identifiant #valeurThermostat
 *
 *Pour d�marrer le chauffage, il faut cliquer le curseur de d�filement
 */
/*********************Ne pas modifier***********************/
$(document).ready(function () {
  $("#thermostat").slider(
    {
      orientation: 'vertical',
      max: 40,
      value: temperatureThermostat,
      min: -10,
      step: 1
    });
  $("#thermostat").slider({
    change: function (event, ui) {
      $("#tdValeurThermostat").text(ui.value);
    }
  });
});
/*********************Ne pas modifier***********************/

/**
 * On instancie tous les objets de notre systeme ici
 */
$(document).ready(function () {
  init();

  /*
   * cree les obervers pour les deux views
   * view 1 : le thermometre
   * view 2 : la boite d'information sur la chambre
   */
  var obsThermo = new ObserverThermo();
  var obsInfo = new ObserverInfo();

  /*
   * Cree l'observable avec un tableau d'observer
   */
  var observableChambre = new ObservableChambre();
  
  /*
   * Ajouter les deux observer a l'observable
   */
  observableChambre.addObs(obsThermo);
  observableChambre.addObs(obsInfo);

  /*
   * Methode setInterval permet de jouer la methode setTimeOut en boucle
   *  -Tictac: verifie s'il a de quoi a modifier dans les vues
   *  -notifyAll: alerter les observers qu'ils doivent updater leur view
   */
  window.setInterval(function() {
    ticTac();
    observableChambre.notifyAll();
  }, intervalleTemps);
});

/**
 * Initie la temperature du thermostat ainsi que la position de notre container
 */
function init() {
  $('#tdValeurThermostat').text(temperatureThermostat);
  $('#mainRow').css('top', positionThermometre + "px");
}
