from LectureFichier import *
from Flotte import *


# Permet d’assigner des colis à un drone en respectant les
# limitations physiques du drone et en s’assurant que tous 
# les colis d’un drone vont vers le même quartier.

class Assign:
    __requeteAssigner = False;
    __listRequetesFail = []
    __listRequetesEnAttente = []

    #__requetesInfo est un tableau de tableau qui regroupe les requetes et les drones utitilise
    # ex:  __requetesInfo = [ [requet1, drone1], [requet2, drone2], [requet3, drone3] ]
    #       
    #       => __requetesInfo[0][0] = requet1 
    #       => __requetesInfo[2][1] = Drone3 
    __requetesInfo = []

    def __init__(self):
        self.__requeteAssigner = False;
        self.__listRequetesFail = []
        self.__requetesInfo = []
        self.__listRequetesEnAttente = []

    def getRequestInfo(self):
        return self.__requetesInfo

    """
    Assigne les colis au drone et fait en sorte que les drones connaissent leurs nouvelles adresses
    et que les adresses de depots connaissent quelles drones elles possedes
    @param  listRequetes: liste des requetes avec l'adresse de depart, de fin et le poids du colis
            listDepots  : Dict des adresse avec leurs drone
            listDrones  : La list des drone dune flotte
    """
    def assignerLesColis(self, listRequetes, listDepots, listDrones):
        #faire sur que la liste de requete manquer est vide au debut
        self.__listRequetesFail = []
        
        if self.__listRequetesEnAttente: 
            print('\n******************************')
            print("Requete en attente ajoutee: ")           
            for element in self.__listRequetesEnAttente:
                print("\nDEMANDE DE REQUÊTE")
                print("\tAdresse de départ :\t", element[0])
                print("\tAdresse d'arrivée :\t", element[1])
                print("\tPoids :\t\t\t", element[2])
                listRequetes.append(element)
            self.__listRequetesEnAttente = []

        #Boucle pour traiter chaque adresse
        for requet in listRequetes:
            #initialise que la requet na pas ete assigner
            self.__requeteAssigner = False;
            
            if requet[0] == requet[1]:
                self.__requeteAssigner = True;
                print('\n=====================================================================')
                print("Puisque la requete livre a elle meme, " , requet[0], " -> ", requet[1], " , aucun drone n'a ete utilisee")   
                print('=====================================================================')

            #Si l'adresse d'entree de la requet est dans la list de depot
            if requet[0] in listDepots:
                depot = requet[0]
                if listDepots[depot][0] is 0 :              #Si le debot na pas de drone
                    self.__listRequetesFail.append(requet)
                    continue
                
                #Pour chaque drone du debot
                for i in range(1, len(listDepots[depot])):                    
                    drone = listDepots[depot][i]
                    
                    #Condition parfaite: respect capacitee et est disponnible
                    if (drone.getPoidsColis() + int(requet[2]) <= drone.getCapacitee()) and drone.getStatus() is True:
                        self.__assigneDrone(drone, requet)            #assigne le drone a la requet
                        self.__requeteAssigner = True                 #requet a ete assigner
                        #Si le poid du drone = celle de ca capacitee
                        if drone.getPoidsColis() == drone.getCapacitee():
                            drone.setStatus(False)          #drone n'est pue dipos
                        self.__affichierRequetInfo(drone,requet)
                        break
                    #Si on a regarde tout les drones du debot et que la requet na toujours pas ete assigner
                    if i is len(listDepots[depot])-1 and self.__requeteAssigner is False:  
                        self.__listRequetesFail.append(requet)

        for requet in self.__listRequetesFail:
            self.__findDrone(requet,listDepots) 
        self.__updateStatus(listDepots,listDrones)            #update le status des drones et le contenue des depot                  

        
    """
    Cherhce dans la liste de depots s'il a un drone de disponnible
    @param  requet  : la requet pour laquelle on doit trouver un drone dispo
            listDepots : la list de depots a regarder
    """
    def __findDrone(self, requet, listDepots):
        self.__requeteAssigner = False
        # ladresse de depart de la requet possede un drone  verifier s'il a un nouveau drone de dispo
        if listDepots[requet[0]][0] is not 0 :
            for data in listDepots[requet[0]]:
                if type(data) is not int:
                    drone = data
                    #Sil trouve un drone qui est dipos et respect les criteres        
                    if (drone.getPoidsColis() + int(requet[2]) <= drone.getCapacitee()) and drone.getStatus() is True:
                        self.__assigneDrone(drone, requet)            #assigne le drone a la requet
                        self.__requeteAssigner = True                 #requet a ete assigner
                        self.__affichierRequetInfo(drone,requet)
                        #Si le poid du drone = celle de ca capacitee
                        if drone.getPoidsColis() == drone.getCapacitee():
                            drone.setStatus(False)          #drone n'est pue dipos
                        return  

        #regarder dans chaque depot
        for depot in listDepots:
            #Si le depot n'est pas celle de ladresse de depart de la requet
            if depot != requet[0] and listDepots[depot][0] is not 0:
                #regarde chaque drone du depot
                for i in range(1, len(listDepots[depot])):                    
                        drone = listDepots[depot][i]
                        #Sil trouve un drone qui est dipos et respect les criteres        
                        if (drone.getPoidsColis() + int(requet[2]) <= drone.getCapacitee()) and drone.getStatus() is True and drone.getNbrColis() is 0:
                            self.__assigneDrone(drone, requet)            #assigne le drone a la requet
                            self.__requeteAssigner = True                 #requet a ete assigner
                            #Si le poid du drone = celle de ca capacitee
                            if drone.getPoidsColis() == drone.getCapacitee():
                                drone.setStatus(False)          #drone n'est pue dipos
                            #Ajouter le drone au bon depot
                            listDepots[requet[0]][0] += 1                                         
                            listDepots[requet[0]].append(listDepots[depot][i])
                            print("\n+++++ Le drone", drone.getId(), "a ete transferer au debot ", requet[0], ' +++++\n' )
                            #Retire le drone du vieux depot
                            listDepots[depot][0] -= 1                                           
                            del listDepots[depot][i]

                            self.__affichierRequetInfo(drone,requet)
                            return  
                    #Si sil a aucun depot disponnible ou drone => requet toujours pas assigner affichier alert
        if self.__requeteAssigner is False:
            self.__listRequetesEnAttente.append(requet)
            print('\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
            print("ECHEC: la requete faite a l'adresse ", requet, " na pas pue etre connectee")
            print('\tElle sera ajoute au prochain cycle de requetes')
            print('\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    """
    Assigne une adresse de debot a un drone selon la distination dune requet
    @param  drone   : Object Drone
            requet  : une requet de la list de requetes
    """     
    def __assigneDrone(self,drone, requet):
        drone.setAdresseDepot(requet[1])                                #assigne nouvelle adresse a drone
        drone.setPoidsColis(drone.getPoidsColis() + int(requet[2]))     #Incremente poids du drone
        drone.setNbrColis(drone.getNbrColis() + 1)                      #Incremente nombre de colis du drone
        drone.incrementerNbrColisLifetime()
        drone.setStandbyTime( drone.getStandbyTime() +1)                #Le standBytime augmente selon le nombre de colis
        self.__addRequetesInfo(drone, requet)

    def __updateStatus(self, listDepots, listDrones):
        #Pour chaque depot de la list dde depots verifier sil possede un mauvais drone
        for depot in listDepots:
            if listDepots[depot][0] is not 0:
                
                i = len(listDepots[depot]) -1
                #pour chaque valeur de la list du depot
                while(i > 0):
                    drone = listDepots[depot][i]
                    # Si le drone qui est dans le depot a pas la meme adresse
                    if drone.getAdresseDepot() is not depot :
                        #Ajouter le drone au bon depot              
                        listDepots[drone.getAdresseDepot()][0] += 1                                         
                        listDepots[drone.getAdresseDepot()].append(drone)
                        #Retire le drone du depot
                        listDepots[depot][0] -= 1                                           
                        del listDepots[depot][listDepots[depot].index(drone)]
                        drone.setStatus(False)
                    i -= 1

    def affichierAllRequetesInfo(self):
        for data in self.__requetesInfo:
            print('\n=====================================================================')
            print('Requete: ', data[0][0], ' -> ', data[0][1], ' : ', data[0][2])
            print('Drone ', data[1].getId(), ': ')
            print('\t\t Capacitee: ', data[1].getCategorie())
            print('\t\t Adresse: ', data[1].getAdresseDepot())
            print('\t\t Status: ', data[1].getStatus())
            print('\t\t Notre total de colis apres cette requete: ', data[1].getNbrColis())  
            print('\t\t Poid avec colis: ', data[1].getPoidsColis())
            print('=====================================================================')

    def __addRequetesInfo(self,drone,requet):
        self.__requetesInfo.append([requet,drone])

    def __affichierRequetInfo(self, drone, requet):
        print('\n=====================================================================')
        print('Requete: ', requet[0], ' -> ',requet[1], ' : ', requet[2])
        print('Drone ', drone.getId(), ': ')
        print('\t\t Capacitee: ', drone.getCategorie())
        print('\t\t Adresse: ', drone.getAdresseDepot())
        print('\t\t Status: ', drone.getStatus())
        print('\t\t Notre total de colis apres cette requete: ', drone.getNbrColis())  
        print('\t\t Poid avec colis: ', drone.getPoidsColis())
        print('=====================================================================')