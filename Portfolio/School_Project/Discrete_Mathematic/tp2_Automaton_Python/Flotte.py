from Drone import *

class Flotte:
    __listDrones = []

    # listDepots est un dictionnaire de list contenant, avec comme keys les adresses et comme valeurs
    # des lists qui contiennes le nombre de drone et les drones 
    # => __listDepots = { adresse: [nbrDrones, Drone1, Drone2]}
    __listDepots = {}

    __nbDronePlace = 0

    def __init__(self):  # constructeur
        self.__listDrones = []
        self.__nbDronePlace = 0
        self.__listDepots = {}

    def getListeDrone(self):
        return self.__listDrones

    def getNbrDrone(self):
        return len(self.__listDrones)

    def getDroneById(self, index):
        return self.__listDrones[index]

    def getListDepots(self):
        return self.__listDepots

    """
    Permet de cree un depot par adresse en initialisant le nombre de drone 
    present au depot a 0
    @param  listAdresse : liste des adresses fournie lors de la creation de l'automate
    """

    def initDepots(self, listAdresse):
        self.__nbDronePlace = 0
        self.__listDepots.clear()
        for drone in self.__listDrones:
            drone.setAdresseDepot('NULL')

        for adresse in listAdresse:
            self.__listDepots.update({adresse: [0]})

    """
    Permet d'ajouter un drone a la flotee
    @param newDrone : objet drone 
    """

    def addDrone(self, newDrone):
        self.__listDrones.append(newDrone)

    """
    Permet d'équilibrer le nombre de drônes presents dans chaque quartier de la ville.
    Critères provenant de Justine :
        1- Chaque cycle fini à equilibrage.
        2- Répartir drône dans des points de dépôts distincts.
        3- D'un cycle à lautre, les drones doivent visiter tous les quartiers.
        4- S'il y a plusieurs livraison dans un dépôt on peut favoriser ce
            dernier en lui donnant plus de drônes.
        5- Un cycle représente une livraison fait par un drone du centre de depot à l'adresse.
        6- Si le drône a plusieurs livraison, cela voudra dire qu'il ne sera pas disponible
            pour l'equilibre pour un cycle.
        7- S'il n'y a aucune livraison à faire, le drône change de centre de dépôt.
    
    """
    def equilibrerFlotte(self):
        # MAJ du status des drônes en fonction de leur état (en standby ou non).
        self.__updateStandbyTime()          # Libère le drône s'il est disponible.
        
        # Boucle qui regarde si des drones ont la même adresse.
        for drone in self.__listDrones:
            if (drone.getStatus() is True): # Vérifie si le drône est disponnible.
                for d in self.__listDrones:
                    adresse = drone.getAdresseDepot()
                    #Verifie (si drone 1 et drone 2 on la même adresse) ,
                    #        (si leur adresse n'est pas 'NULL') ,
                    #        (si le nombre de drône à l'adresse ne depasse pas le nombre de drône à placer) ,
                    #        (si le deuxieme drône est disponible).
                    if drone.getAdresseDepot() is d.getAdresseDepot() and adresse is not 'NULL' and self.__listDepots[adresse][0] >  self.__nbDronePlace and d.getStatus() is True:
                        self.__listDepots[drone.getAdresseDepot()][0] -= 1                          # Réduit le nombre de drône à l'adresse.
                        del self.__listDepots[adresse][ self.__listDepots[adresse].index(drone)]    # Retire le drône de la liste de l'adresse.
                        drone.setAdresseDepot('NULL')                                               # Met l'adresse du drône à 'NULL.
                        break
        # Boucle pour attribuer des drônes aux adresses sans drone et reduit le temps de standby.
        for drone in self.__listDrones:
            if drone.getAdresseDepot() is 'NULL':       # Si l'adresse du drone est 'NULL' ,
                self.__giveDepotDrone(drone)            # trouver et donner une adresse disponible au drône.
                if drone.getAdresseDepot() is 'NULL':   # Si le drône n'a toujours pas d'adresse ,
                    self.__nbDronePlace += 1            # augmenter le nombre de drône par adresse.
                    self.__giveDepotDrone(drone)        # Trouver et donner une adresse disponible au drône.


    def __giveDepotDrone(self, drone):
        # Boucle qui regarde toutes les adresses de depôt pour trouver une adresse qui peut accepter un drône.
        for depot in self.__listDepots:
            # Si le nombre de drône dans l'adresse respecte le nombre de drône pouvant être placer et que le drone est disponible.
            if self.__listDepots[depot][0] is self.__nbDronePlace and drone.getStatus():
                drone.setAdresseDepot(depot)            # Donner l'adresse au drône.
                self.__listDepots[depot].append(drone)  # Ajoute le drône au dépôt.
                self.__listDepots[depot][0] += 1        # Augmente le nombre de drône au dépôt.
                break


    def __updateStandbyTime(self):
        for drone in self.__listDrones:
            if drone.getStandbyTime()  > 0:
                drone.setStandbyTime(drone.getStandbyTime() - 1)
            if drone.getStandbyTime() is 0:
                drone.setNbrColis(0)
                drone.setPoidsColis(0)
                drone.setStatus(True)
            