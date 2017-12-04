from LOG2810_TP1_PYTHON import *

import os

# Permetl'affichage du menu principal.
def affichierMenu():
    print('------- Menu Principal -------')
    print('(a) Drones\n(b) Recettes\n(c) Quitter')
    print('------------------------------')
    print('Rentrer commande: ', end="")

# Demande à l'utilisateur d'entrer une commande à la console.
def demanderCmd():
    print('Rentrer commande: ', end="")

# Libère la console de tout écriture.  Deux version existent ; une pour Linux
# et une deuxième pour Windows.
def clearScreen():
    os.system('clear')                      # Version pour Linux.
    # os.system('cls')                      # Version pour Windows.

# ==== CORE ====
affichierMenu()
while True:
    cmd = input()
    if cmd == 'a' or cmd =='A':             # L'UTILISATEUR SÉLECTIONNE LE PROGRAMME DRÔNES.
        clearScreen()
        menuDrone();
        clearScreen()
        affichierMenu()
    elif cmd == 'b' or cmd =='B':           # L'UTILISATEUR SÉLECTIONNE LE PROGRAMME DES RECETTES.
        print('\n!ATTENTION!')
        print('Puisque le code de la section \'Recettes\' est en c++,\nil faut l\'activer manuellement.\n')
        affichierMenu();
    elif cmd == 'c' or cmd =='C':           # L'UTILISATEUR VEUT QUITTER.
        exit()                              # Permet de fermer la fenêtre.
    else:
        print('\nVous navez pas entré une commande valide... \n\n')
        affichierMenu()