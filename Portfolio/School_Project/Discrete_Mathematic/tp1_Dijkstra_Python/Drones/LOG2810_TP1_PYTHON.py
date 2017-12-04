import os.path as osp

from map import *
from parcours import *

def afficherMenu():
    print('--------------------- Menu ---------------------')
    print('(a) Mettre à jour la carte\n(b) Déterminer le plus court chemin sécuritaire\n(t) Rouler une série de tests\n(c) Quitter')
    print('------------------------------------------------')
    print('Entrez commande: ', end="")
def demanderCmd():
    print('Entrez commande: ', end="")

def menuDrone():
    #Affiche le menu et attend pour un input
    afficherMenu()
    carteMisAJour = False
    while True:
        cmd = input()
        print()
        if cmd == 'a' or cmd =='A':                                     # METTRE À JOUR LA CARTE.
            print('Entrer le lien vers le fichier texte : ', end="")
            link = input()
            print()
            if osp.isfile(link):                                        # Vérifie si le fichier existe.
                carteMisAJour = True
                g = Graphe()
                g.creeGraphe(link)                                      # Création du graphe à partir du fichier.
                g.affichierGraphe()                                     # Affichage de la map en format matrice.
                g.afficherGraphiqueLigne()                              # Affichage de la map en format chaine de caractères.
                print('')
                afficherMenu()
            else:                                                       # Retour au menu si la lecture du fichier échoue.
                print('\nERROR: le fichier n\'existe pas\n')
                afficherMenu()
                demanderCmd()

        elif (cmd == 'b' or cmd =='B') and carteMisAJour is True:                                   # PLUS COURT CHEMIN.
            chemin = Chemin(g)

            # Sélection du point de départ par l'utilisateur.
            print('Point de départ : ', end = "")
            pointDepart = int(input())
            while pointDepart < 0 or pointDepart > 19:
                print('Votre point de départ est hors borne.')
                print('Veuillez entrer un point de départ valide : ', end = "")
                pointDepart = int(input())
            print()
            
            # Sélection du point d'arrivé par l'utilisateur.
            print('Point d\'arrivé : ', end = "")
            pointArrive = int(input())
            while (pointArrive < 1 or pointArrive > 19) or pointArrive == pointDepart:
                if pointArrive == pointDepart:                          # On refuse si le point d'arrivée et le point de départ sont égaux.
                    print('Votre point d\'arrivé est le même que celui de départ.')
                else:                                                   # On refuse si les point d'arrivée est hors borne.
                    print('Votre point d\'arrivé est hors borne.')
                print('Veuillez entrer un point d\'arrivé valide : ', end = "")
                pointArrive = int(input())
                print()

            # Sélection du type de colis par l'utilisateur.
            print('Sélectionnez le type de colis.  Les choix sont :\n\tplume\n\tmoyen\n\tlourd')
            print('Veuillez entrer votre sélection : ', end = "")
            typeColis = input()
            while typeColis != 'plume' and typeColis != 'moyen' and typeColis != 'lourd':
                print('Veuillez entrer une sélection valide : ', end = "")
                typeColis = input()
            
            # Calcul du chemin le plus court.
            chemin.plusCourtChemin(pointDepart, pointArrive, typeColis, '3.3')
            
            print()
            afficherMenu()
            demanderCmd()

        elif cmd == 'c' or cmd =='C':                                   # QUITTER LE PROGRAMME.
            break;

        elif (cmd == 'b' or cmd =='B') and carteMisAJour is False:      # TENTATIVE DE CALCULER UN CHEMIN SANS AVOIR CHARGÉ DE CARTE EN MÉMOIRE.
            print('!Attention!\nVeuillez tout d\'abord charger une carte avec l\'option a) .\n')
            afficherMenu()
        
        elif(cmd == 't'):
            # Load le fichier.
            link = 'arrondissements.txt'
            if osp.isfile(link):                                        # Vérifie si le fichier existe.
                carteMisAJour = True
                g = Graphe()
                g.creeGraphe(link)                                      # Création du graphe à partir du fichier.
                g.affichierGraphe()                                     # Affichage de la map en format matrice.
                g.afficherGraphiqueLigne()                              # Affichage de la map en format chaine de caractères.
            else:                                                       # Retour au menu si la lecture du fichier échoue.
                print('\nERROR: le fichier n\'existe pas\n')
                afficherMenu()
                demanderCmd()
                break;

            # Roule une série de tests.
            print('\nPour quel point de départ voulez-vous générer le test ? ', end = "")
            cpt = int(input())
            while cpt < 0 or cpt > 19:
                print('\nVotre point de départ est hors borne.')
                print('Veuillez entrer un point de départ valide : ', end = "")
                cpt = int(input())
            print()

            cpt2 = 1
            while cpt2 < 20:
                print('\nPoint de dépat : ', cpt, '\nPoint d\'arriver : ', cpt2)
                if cpt2 is not  cpt :
                    chemin = Chemin(g)
                    chemin.plusCourtChemin(cpt, cpt2, 'plume', '3.3')
                    chemin = Chemin(g)
                    chemin.plusCourtChemin(cpt, cpt2, 'moyen', '3.3')
                    chemin = Chemin(g)
                    chemin.plusCourtChemin(cpt, cpt2, 'lourd', '3.3')
                cpt2 += 1

            print()
            afficherMenu()
            demanderCmd()

        else:                                                           # COMMANDE NON VALIDE AU MENU.
            print('\nVous n\'avez pas entré une commande valide...\n\n')
            afficherMenu()