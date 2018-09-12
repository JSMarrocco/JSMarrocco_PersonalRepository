from map import *
from Drone import *

class Chemin(object):
    graphe_ = Graphe()

    def __init__(self, graphe):                     # Constructeur.
        self.graphe_ = graphe
        self.tempsComplet = 0
        self.cantGo = []
        self.sommetsParcourus = []


    def verifierBatterie(self):
        if (self.drone.batterie_ <= 20):
            return False
        else:
            return True
    

    def dijkstra(self, startPoint, finishPoint, searchBorne):
        visited = {startPoint: 0}                   # Liste des noeuds visités, seul le 'startPoint' est visité au départ.
        path = {}
        path_weight = 999
        cheminCours = {}
        noeud_borne = 0
        noeuds = set(self.graphe_.noeuds)           # Crée une liste avec tous les sommets.
          
        while noeuds:                               # Tant qu'il y a des noeuds dans le tableau...
            min_noeud = None
            for noeud in noeuds:                    # Choisi le noeud le plus petit qui est en 'noeuds' et 'visited'.
                if noeud in visited:
                    if min_noeud is None:
                        min_noeud = noeud
                    elif visited[noeud] < visited[min_noeud]:
                        min_noeud = noeud
            if min_noeud is None:                   # Si 'min_noeud' est 'None' , alors cela veut dire que 'noeuds' est vide.
                break
            noeuds.remove(min_noeud)                # Retire le 'min_noeurd' de 'noeuds' et lui donne un poids.
            current_weight = visited[min_noeud]
            for arc in self.graphe_.arcs[min_noeud]:                                # Regarde tous les arcs reliés au 'min_noeud'.
                weight = current_weight + self.graphe_.distances[(min_noeud,arc)]   # Met à jour le poids de ce chemin.
                if arc not in visited or weight < visited[arc]:                     # Si l'arc n'est pas dans la liste 'visited' ou a un poids plus petit...
                    visited[arc] = weight                                           # Ajouter/mettre à jour le poids du noeuds à cet arc et ajoute au chemin 'path' possible.
                    path[arc] = min_noeud
                    if searchBorne is False:                                        # Vérifie si on cherche un borne de rechargement ou non.
                        if arc is finishPoint and weight < path_weight:             # Si on a trouvé un point final, verifier si on a trouvé un meilleur chemin.                    
                            path_weight = weight
                            cheminCours[arc] = min_noeud
                    else:
                        # Vérifie qu'on n'a pas déjà visité cette option de borne.
                        if self.graphe_.listSommet[arc - 1].peuRecharger_ is 1 and weight < path_weight and arc not in self.cantGo:
                            cheminCours = {}
                            path_weight = weight
                            cheminCours[arc] = min_noeud
                            noeud_borne = arc      
        if searchBorne is False:                            # Vérifier si on trouvé un borne ou le point final.
            point = cheminCours[finishPoint] 
        else:
            point = cheminCours[noeud_borne] 
        # Permet d'obtenir le chemin complet du 'cheminCours' trouvé.
        trouverDebut = False
        while(trouverDebut is not True):
            for node in path:
                if node is point:
                    cheminCours[node] = path[node]
                    point = path[node]
                if point is startPoint:
                    trouverDebut = True
        return cheminCours, path_weight


    def plusCourtChemin(self,startPoint, finishPoint,typeColis,typeDrone):
        self.drone = Drone(typeDrone)
        self.drone.batterie_ = 100          # Niveau de charge de la pile du drone.
        self.cantGo = []                    # Endroit où le drone ne peut passer (chemin non efficace).
        self.sommetsParcourus = []          # Énumération des sommets parcourus par le drone pour le chemin le plus rapide.
        canMakeIt = True                    # Un booléen indiquant si le drone peut se rendre du point de départ au point d'arrivé.
        utilisationPile = 0;                # Variable utilisée pour le calcul du temps d'utilisation complet du drone.
        tmpArray = []                       # Variable utilisée pour faciliter le remplissage du tableau 'sommetsParcourus'.

        # Vérifier si on se trouve sur une borne de rechargement au départ.
        if self.graphe_.listSommet[startPoint-1].peuRecharger_ is 1 and self.drone.type_ == '3.3':
            self.graphe_.nbrBorne -= 1

        # Vérifier s'il est possible de se rendre d'un coup du point A au point B.
        cheminCourt, temps = self.dijkstra(startPoint,finishPoint,False)        # Retournera le chemin le plus court et le temps pour passer du point A au point B.
        self.drone.utiliserBatterie(typeColis,temps)                            # On calcule l'utilisation de la pile pour passer du point A au point B.
        utilisationPile = temps;
        if self.verifierBatterie() is False:                                    # L'utilisation de la pile dépasse ça capacité.
            for nbrBorne in range(0,self.graphe_.nbrBorne):
                self.drone.batterie_ = 100     
                # Recherche borne.  Vérifier s'il est possible de se rendre d'un coup du point A à une borne de rechargement.
                cheminCourt, temps = self.dijkstra(startPoint,0,True)           # Retournera le chemin et le temps pour passer du point A à la borne de recharge la plus près.
                self.drone.utiliserBatterie(typeColis,temps)                    # Calcule de l'utilisation de la pile pour ce trajet.
                utilisationPile = temps  
                for arc in cheminCourt:                                         # On ajoute les sommets parcourus jusqu'à la borne de rechargement au tableau 'tmpArray'.
                    tmpArray.append(arc)
                if self.verifierBatterie() is False:                            # L'utilisation de la pile dépasse la capacité du drone.
                    self.cantGo.append(list(cheminCourt.keys())[0])
                    canMakeIt = False
                    tmpArray = []
                else:                                                           # L'utilisation de la pile ne dépasse pas la capacité du drone.  On peut se rendre à la borne de recharge la plus près.
                    self.drone.batterie_ = 100                                  # Recharge de la pile.
                    utilisationPile += 20                                       # 20 minutes pour la recharge de la pile.
                    #Recherche du point B.  Vérifier s'il est possible de se rendre d'un coup de la borne de recharge au point B.
                    cheminCourt, temps = self.dijkstra(list(cheminCourt)[0],finishPoint,False)  # Calcule du chemin le plus court et le temps pour se rendre de la borne de recharge au point B.
                    self.drone.utiliserBatterie(typeColis,temps)                # Calcule de l'utilisation de la pile pour ce trajet.
                    utilisationPile += temps            
                    tempSecondArray = []
                    for arc in cheminCourt:
                        tempSecondArray.append(arc)
                    if self.verifierBatterie() is False:                        # Meme en allant se recharger, le drone ne se rendra pas au point B.
                        self.cantGo.append(list(cheminCourt.values())[len(cheminCourt) - 1])
                        canMakeIt = False
                        tmpArray = []
                    else:                                                       # Le drone peut rejoindre le point B.
                        canMakeIt = True
                        self.tempsComplet += utilisationPile                    # On incrémente le temps d'utilisation du drone au temps complet.
                        nb = len(tmpArray) - 1
                        self.sommetsParcourus = []
                        self.sommetsParcourus.append(startPoint)
                        while nb >= 0:                                          # On place dans le bon ordre les sommets parcourus.  Le premiers en début de tableau.
                            self.sommetsParcourus.append(tmpArray[nb])
                            nb -= 1
                        nb = len(tempSecondArray) - 1
                        while nb >= 0:                                          # On place dans le bon ordre les sommets parcourus.  Le premiers en début de tableau.
                            self.sommetsParcourus.append(tempSecondArray[nb])
                            nb -= 1
                        break
        else:                                                                   # Le drone se rend du point A au point B sans avoir besoin de recharge.
            self.tempsComplet += utilisationPile
            self.transfertSommetsParcourus(tmpArray, cheminCourt, startPoint)   # Permet de transférer les sommets se trouvant dans le tableau tmpArray vers sometsParcourus, et dans le bon ordre.
        if canMakeIt is False:                                                  # Cas où le drone ne peut se rendre.
            if self.drone.type_ == '3.3':
                self.plusCourtChemin(startPoint,finishPoint,typeColis,'5.0')    # On test le même parcourt, mais avec le drone type 5.0 .
            else:
                print('******************************************************')
                print('* Désolé, mais cette livraison ne sera pas possible. *')
                print('******************************************************')
                return
        else:
            print('********************************************')
            print('* Drone utilisé :\t', self.drone.type_)
            print('* Type du colis :\t', typeColis)
            print('* Temps complet :\t', self.tempsComplet,'min')
            print('* Pile :\t\t', self.drone.batterie_, '%')
            print('* Parcours emprunté:\t ', end = "")
            self.afficherSommetsParcourus()
            print('********************************************')


    def transfertSommetsParcourus(self, tmpArray, cheminCourt, startPoint):
        for arc in cheminCourt:
            tmpArray.append(arc)
        nb = len(tmpArray) - 1
        self.sommetsParcourus = []
        self.sommetsParcourus.append(startPoint)
        while nb >= 0:                                          # On place dans le bon ordre les sommets parcourus.  Le premiers en début de tableau.
            self.sommetsParcourus.append(tmpArray[nb])
            nb -= 1


    def afficherSommetsParcourus(self):
        nbElement = len(self.sommetsParcourus)
        result = ""
        result = str(self.sommetsParcourus[0])
        cpt = 1;
        while cpt < nbElement:
            result += ' -> '
            result += str(self.sommetsParcourus[cpt])
            cpt += 1
        print(result)
