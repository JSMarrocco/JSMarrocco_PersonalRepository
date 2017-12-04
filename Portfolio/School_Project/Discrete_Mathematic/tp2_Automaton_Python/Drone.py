# Catégorie 1 : Jusqu'à 1 kg
# Catégorie 2 : Jusqu'à 5 kg
class Drone:
    __categorie = ""
    __status = ""
    __nbrColis = 0
    __poidsColis = 0
    __id = ""
    __capacitee = ""
    __adresseDepot = ""
    __standbyTime = 0

    # Constructeur.
    def __init__(self, id_, categorie, status):
        self.__categorie = categorie
        self.__status = status
        self.__nbrColis = 0
        self.__nbrColisLifetime = 0
        self.__poidsColis = 0
        self.__id = id_
        self.__adresseDepot = 'NULL'
        self.__standbyTime = 0;

        #assigne la bonne capacitee pour la bonne categorie
        if self.__categorie is 1:
            self.__capacitee = 1000
        elif self.__categorie is 2:
            self.__capacitee = 5000

    #setter
    def setStatus(self, status):
        self.__status = status

    def setNbrColis(self, nbrColis):
        self.__nbrColis = nbrColis

    def setPoidsColis(self, poidsColis):
        self.__poidsColis = poidsColis
    
    def setAdresseDepot(self, adresseDepot):
        self.__adresseDepot = adresseDepot

    def setStandbyTime(self, standbyTime):
        self.__standbyTime = standbyTime

    def setNbrColisLifeTime(self, nb):
        self.__nbrColisLifetime = nb

    #Getter
    def getStatus(self):
        return self.__status

    def getNbrColis(self):
        return self.__nbrColis

    def getNbrColisLifetime(self):
        return self.__nbrColisLifetime

    def getCategorie(self):
        return self.__categorie

    def getPoidsColis(self):
        return self.__poidsColis

    def getId(self):
        return self.__id

    def getAdresseDepot(self):
        return self.__adresseDepot

    def getCapacitee(self):
        return self.__capacitee

    def getStandbyTime(self):
        return self.__standbyTime

    def incrementerNbrColisLifetime(self):
        self.__nbrColisLifetime += 1