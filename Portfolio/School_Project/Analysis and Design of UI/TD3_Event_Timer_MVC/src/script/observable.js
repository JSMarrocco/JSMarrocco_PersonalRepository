/**
 * Classe qui represente le controleur de la chambre
 *
 * @classdesc
 */
class ObservableChambre {
    /**
     * Initie une liste de plusieurs observers
     *
     * @constructor 
     */
    constructor() {
        this.observers = [];
    }

    /**
     * Alerte chaque observer du tableau observers et leur envoies les 
     * informations fournies par le modele (chambre) 
     *
     */
    notifyAll() {
        var infoChambre = {
            'temperatureInterieure': temperatureInterieure,
            'chauffage': chauffage,
            'thermometreMax':thermometreMax
        };
        this.observers.forEach(function (e) {
            e.updateObs(infoChambre)
        });
    }

    /** 
     * Permet d'ajouter des observers au tableau
     *
     * @param {*} obs - observer de la classe
     */
    addObs(obs) {
        this.observers.push(obs);
    }


}