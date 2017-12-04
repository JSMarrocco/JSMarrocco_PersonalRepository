import os

"""
Permet de lire un fichier de codes postaux et de les renvoyer sous forme de tableau.
Chaque adresse postale du fichier devient une position dans le tableau d'adresses.
@param nomFichier   : Nom du fichier pour lequel on veut récupérer les codes postaux.
@return             : Le tableau contenant les codes postaux dans le fichier.
"""
def lectureFichierUnElementParLigne(nomFichier):
    adresses = []                               # Initialisation du tableau d'adresses postales.
    
    with open(nomFichier, "r") as f:            # Ouvrir le fichier.
        for line in f:                          # Lire chaque ligne.
            adresses.append(line.rstrip('\n'))  # Retrait du retour à la ligne & ajout au tableau d'adresses.
        
    return adresses


"""
Permet de lire un fichier de requêtes et de les renvoyer sous forme de tableau.
La variable 'requetes' est sous la forme suivant :
    -> [ [ *adresse de départ* , *adresse d'arrivée* , *poids* ] , [...] , [...] , ... ]
@param nomFichier   : Nom du fichier pour lequel on veut récupérer les requêtes.
@return             : Le tableau contenant les requêtes présentes dans le fichier.
"""
def lectureFichierRequete(nomFichier):
    requetes = []                                   # Tableau qui contiendra chacune des requetes.
    
    with open(nomFichier, "r") as f:                # Ouverture du fichier.
        for line in f:                              # Parcourt de chaque ligne du fichier.
            line.rstrip('\n')                       # Retrait de la fin de ligne.
            requete = line.split()                  # Split la ligne a chaque espace.
            requetes.append(requete)
    
    return requetes