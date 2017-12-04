from TraiterRequetes import *
from AssignationColis import *
from CreationArbreAdresses import *
from Drone import *
from Flotte import *
from pathlib import Path


def afficherChoixMenu():
    print("\n*************************************************************")
    print("*\t\t\t\t\t\t\t    *")
    print("*\t\t\t    MENU\t\t\t    *")
    print("*\t\t\t\t\t\t\t    *")
    print("*************************************************************")
    print("*\t\t\t\t\t\t\t    *")
    print("* (a) Créer l’automate.\t\t\t\t\t    *")
    print("* (b) Traiter des requêtes.\t\t\t\t    *")
    print("* (c) Afficher les statistiques.\t\t\t    *")
    print("* (d) Quitter.\t\t\t\t\t\t    *")
    print("*\t\t\t\t\t\t\t    *")
    print("*************************************************************")


def creeFlotte(flotte):                 # Crée la flotte selon l'énoncée.
    for index in range (0,10):          # Crée 10 drones de categorie 1 avec le status disponible.
        newDrone = Drone(index,1,True)
        flotte.addDrone(newDrone)
    for index in range (10, 15):        # Crée 5 drones de categorie 2 avec le status disponible.
        newDrone = Drone(index,2,True)
        flotte.addDrone(newDrone)


def imprimerLesStatistiques(listeQuartiers, listeDrones, nbRequetesValides, nbRequetesInvalides):
    nbRequetesTotales = nbRequetesInvalides + nbRequetesValides
    nbColisTotauxCatUn = 0
    nbColisTotauxCatDeux = 0
    nbDronesCategorieUn = 0
    nbDronesCategorieDeux = 0

    for drone in listeDrones:
        if not drone.getNbrColisLifetime() is 0:
            if drone.getCategorie() == 1:
                nbColisTotauxCatUn += drone.getNbrColisLifetime()
                nbDronesCategorieUn += 1
            elif drone.getCategorie() == 2:
                nbColisTotauxCatDeux += drone.getNbrColisLifetime()
                nbDronesCategorieDeux += 1

    if nbDronesCategorieUn is 0:            # Gestion d'erreur arithmétique pour une division par zéro.
        nbMoyenColisCatUn = 0
    else:
        nbMoyenColisCatUn = (nbColisTotauxCatUn / nbDronesCategorieUn)
    
    if nbDronesCategorieDeux is 0:          # Gestion d'erreur arithmétique pour une division par zéro.
        nbMoyenColisCatDeux = 0
    else:
        nbMoyenColisCatDeux = (nbColisTotauxCatDeux / nbDronesCategorieDeux)

    print("\n*************************************************************")
    print("*\t\t\t\t\t\t\t    *")
    print("*\t\tAFFICHAGE DES STATISTIQUES\t\t    *")
    print("*\t\t\t\t\t\t\t    *")
    print("*************************************************************")
    print("\nREQUETES TRAITEES :\t", nbRequetesTotales)
    print("REQUËTES VALIDES :\t", nbRequetesValides)
    print("REQUETES INVALIDES :\t", nbRequetesInvalides)
    print("\n*************************************************************")
    print("\n\t\tREPARTITION DE LA FLOTTE\n")
    print("-------------------------------------------------------------")
    print("| Quartier | Drones faible capacite | Drones forte capacite |")
    print("-------------------------------------------------------------")

    for quartier in listeQuartiers:
        print("| ", quartier, " | ", end = "")
        nbDronesDansQuartierCourant = int(listeQuartiers[quartier][0])
        nbDronesCategorieUn = 0
        nbDronesCategorieDeux = 0

        if nbDronesDansQuartierCourant > 0:         # Récupération du nombre de drones dans le quartier selon leur catégorie.
            for i in range(1 ,  len(listeQuartiers[quartier])):
                if listeQuartiers[quartier][i].getCategorie() is 1:
                    nbDronesCategorieUn += 1
                else:
                    nbDronesCategorieDeux += 1
        print("          ",nbDronesCategorieUn, "          |          ", nbDronesCategorieDeux, "          |")
        print("-------------------------------------------------------------")

    print("\n*************************************************************")
    print("\nNOMBRE MOYEN DE COLIS PAR DRONE : ")
    print("FAIBLE CAPACITE :\t", nbMoyenColisCatUn)
    print("FORTE CAPACITE :\t", nbMoyenColisCatDeux)
    print("\n*************************************************************")


def obtenirNomFichier():
    nomFichier = input()
    while (not os.path.exists(nomFichier) or Path(nomFichier).is_dir()) and (nomFichier != 'q' and nomFichier != 'Q'):
        print("Le fichier mentionné n'a pas été trouvé.")
        print("Entrez le nom du fichier (ou 'q' pour annuler) : ", end="")
        nomFichier = input()

    return nomFichier


def main():
    os.system('clear')  
    listeAdresses = []                      # Contiendra les codes postaux.
    arbreAdresse = ArbreAdresses()
    flotte = Flotte()                       # Crée une flotte.
    creeFlotte(flotte)                      # Ajoute les 15 drones.
    adressesChargees = False
    requetesFichier = []
    assign = Assign()
    cptRequetesInvalides = 0
    cptRequetesValides = 0

    while(True):
        afficherChoixMenu()
        print("\nVeuillez entrer votre choix : ", end="")
        cmd = input()
        print()
        
        if cmd == 'a' or cmd == 'A':                                # ============= CRÉER AUTOMATE =============
            print("Veuillez entrer le nom du fichier (ou 'q' pour annuler) : ", end ="")
            nomFichier = obtenirNomFichier()                        # Obtenir un nom de fichier valide.
            if nomFichier == 'q' or nomFichier == 'Q':
                print("La saisie du fichier est abandonnée.  Retour au menu principal.")
                continue
            arbreAdresse.creerArbreAdresses(nomFichier)             # Lit le fichier pour créer l'automate.
            flotte.initDepots(arbreAdresse.getListeAdresses())      # Initialise les dépots (un dépots = un quartier).
            flotte.equilibrerFlotte()                               # Équilibrer la flotte.
            adressesChargees = True                                 # Permet maintenant l'option b) .
        elif (cmd == 'b' or cmd == 'B') and adressesChargees:       # ================ TRAITER REQUÊTES =============
            print("Veuillez entrer le nom du fichier : ", end ="")
            nomFichier = obtenirNomFichier()
            if nomFichier == 'q' or nomFichier == 'Q':
                print("La saisie du fichier est abandonnée.  Retour au menu principal.")
                continue
            requetesFichier, cptReqInv, cptReqVal = traiterLesRequetes(nomFichier, arbreAdresse)
            cptRequetesInvalides += cptReqInv
            cptRequetesValides += cptReqVal
            assign.assignerLesColis(requetesFichier, flotte.getListDepots(), flotte.getListeDrone())
            flotte.equilibrerFlotte()
        elif cmd == 'c' or cmd == 'C':                              # ============= AFFICHER STATISTIQUES =============
            imprimerLesStatistiques(flotte.getListDepots(), flotte.getListeDrone(), cptRequetesValides, cptRequetesInvalides)
        elif cmd == 'd' or cmd == 'D':                              # ============= QUITTER PROGRAMME =============
            print("GOODBYE.\n")
            exit()
        elif (cmd == 'b' or cmd == 'B') and not adressesChargees:
            print("Vous devez d'abord créer l'automate - choix (a).")
            sleep(2.5)                                              # Pause de 2.5 secondes.
        else:
            print("*ATTENTION*\nVous avez entré un choix invalide.\nVeillez saisir à nouveau votre choix.")
            sleep(1)


if __name__ == '__main__' :
    main()