/**
 * Classe qui represente la vue du thermometre
 *
 * @classdesc
 */
class ObserverThermo{
    /**
     * Initie les informations graphiques du thermometre
     *
     * @constructor
     */
    constructor() {
        $('#myTemp').text(temperatureInterieure.toFixed(0));
        $('#myTemp').css('width', (temperatureInterieure + thermometreMax) + "%");
        $('#tempProgress').css('top', (positionThermometre + tailleThermometre / 3.25) + "px");
        $('#tempProgress').css('width', tailleThermometre + "px");
    }

    /**
     * Permet de mettre a jour les informations de la vue
     *
     * @param {*} infoChambre - information concernant la chambre
     */
    updateObs(infoChambre) {
        $('#myTemp').text(infoChambre.temperatureInterieure.toFixed(0));
        $('#myTemp').css('width', (infoChambre.temperatureInterieure + infoChambre.thermometreMax) + "%");
    }
}

/**
 * Classe qui represente l'information sur le systeme
 *
 * @classdesc
 */
class ObserverInfo{
    /**
     * Initie les informations graphiques d'information
     *
     * @constructor 
     */
    constructor() {
        $('#alertActif').css('background-color', 'red');
        $('#alertActif').text('ACTIF');
    }

    /**
     * Permet de mettre a jour les informations de la vue
     *
     * @param {*} infoChambre - information concernant la chambre
     */
    updateObs(infoChambre) {
        if (infoChambre.chauffage) {
            $('#alertActif').css('background-color', 'red');
            $('#alertActif').text('ACTIF');
        } else {
            $('#alertActif').css('background-color', 'white');
            $('#alertActif').text('INACTIF');
        }
    }
}