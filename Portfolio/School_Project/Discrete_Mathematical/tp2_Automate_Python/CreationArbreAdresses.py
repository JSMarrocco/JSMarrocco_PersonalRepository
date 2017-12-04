from LectureFichier import *
from Automate import *
from time import *

"""
Fonctions contenues par la classe ArbreAdresses :
    -> getListeAdresses()
    -> creerArbreAdresses(nomFichier)
    -> validationAdressePostale(adressePostale)
    -> afficherPossibilitesListeAdresses()
    -> contientAdressePostale(adressePostale)
"""

class ArbreAdresses():

    """
    Constructeur par défaut.  Initialisation des attributs de la classe.
    """
    def __init__(self):
        self.__automate = Automate()
        self.__listeAdresses = []


    """
    Permet de retourner la valeur de l'attribut '__listeAdresses'.
    @return : L'attribut '__listeAdresses'.
    """
    def getListeAdresses(self):
        return self.__listeAdresses


    """
    Lit le fichier texte contenant des adresses postales et  crée l’automate responsable
    de valider les codes postaux soumis par les clients pour la livraison d’un colis.
    @param nomFichier  : Nom du fichier a a partir duquel on veut creer l'arbre d'adresses.
    """
    def creerArbreAdresses(self, nomFichier):
        self.__listeAdresses = lectureFichierUnElementParLigne(nomFichier) # La validation de l'adresse postale se fait dans la classe Automate.
        cptAdressesInvalides = 0
        for codePostale in self.__listeAdresses:
            self.__automate.ajouterPossibilites(codePostale)


    """
    Permet de valider une adresse postale.
    À noter que le processus de validation de l'adresse postale se fait dans la classe Automate.
    @param  adressePostale  : Adresse postale qu'on veut valider.
    @return                 : 'True' si l'adresse est valide. 'False' sinon.
    """
    def validationAdressePostale(self, adressePostale):
        return self.__automate.validerFormatAdressePostale(adressePostale)


    """
    Affiche l'automate, c'est-à-dire toutes les possibilités pour chacun des six noeuds
    d'une adresse postale.
    À noter que la logique de cette affichage se trouve dans la classe Automate.
    """
    def afficherPossibilitesListeAdresses(self):
        self.__automate.afficherPossibilites()


    """
    Fonction qui permet de savoir si une adresse postal se trouve dans la
    liste d'adresses postales valides.  Appel simplement la fonction
    'contient adressePostale' de la classe 'Automate'.  
    @param adressePostale   : L'adresse pour laquelle on veut savoir si elle se trouve dans l'automate.
    @return                 : 'True' si l'adresse postale se trouve dans l'automate.
    """
    def contientAdressePostale(self, adressePostale):
        return self.__automate.contientAdressePostale(adressePostale)