/* Simule les variations de temp�ratures dans une pi�ce
 * @auteur: francois.lemieux@polymtl.ca 2010-07-26
*/
var facteurChauffage      = 0.01;  // �change calorifique avec le chauffage
var facteurIsolation      = 0.01;  // �change calorifique avec l'ext�rieur
var temperatureChauffage  = 70;    // temp�rature des calorif�res
var temperatureExterieure = 0;     // temp�rature ext�rieure
var temperatureInterieure = 10;    // temp�rature int�rieure par d�faut
var chauffage             = false; // le chauffage n'est pas actif par d�faut
var temperatureThermostat = 20;       // le chauffage d�marre �  moins de 20� par d�faut

var thermometreMax        =50      // Temp�rature maximale affich�e par le thermom�tre
var thermometreMin        =-50     // Temp�rature minimale affich�e par le thermom�tre
var intervalleTemps       =1000;   // intervalle en milisecondes de lecture de la temp�rature
var tailleThermometre     =300;    // Taille du thermom�tre en pixels
var positionThermometre   =50;     // Position du thermom�tre par rapport au haut de la page

/**Extrait la temp�rature r�gl�e par le thermostatr */
function getTemperatureThermostat(){
  return document.getElementById("tdValeurThermostat").innerHTML;
}

/** D�finit les �changes calorifiques selon les valeurs
 * de la tempp�rature ext�rieure, de l'isolation,
 * de la temp�rature int�rieure, de la temp�rature fix�e
 * par le thermostat et par l'efficacit� du syst�me
 * de chauffage.
 * Un "ticTac" correspond �  un �change calorifique
 */
function ticTac() {
  temperatureInterieure += ((temperatureExterieure - temperatureInterieure) * facteurIsolation);

  if (chauffage == true) {
    temperatureInterieure += ((temperatureChauffage - temperatureInterieure) * facteurChauffage);

    if (temperatureInterieure > getTemperatureThermostat()) {
      chauffage=false;
    }
  } else if (temperatureInterieure < getTemperatureThermostat()) {
    chauffage=true;
  }
}
