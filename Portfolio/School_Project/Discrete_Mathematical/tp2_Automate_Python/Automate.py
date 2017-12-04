from Noeud import *

"""
Fonctions contenues par la classe Automate :
    -> ajouterPossibilites(adressePostale)
    -> validerFormatAdressePostale(adressePostale)
    -> validerFormatCaractere(estUneLettre, caractere)
    -> contientAdressePostale(adressePostale)
    -> afficherPossibilites()
"""

class Automate():

    """
    Constructeur par défaut.  Initialisation des attributs de la classe.
    """
    def __init__(self):                             
        self.__nombreDeNoeuds = int(6)
        self.__noeuds = [ [Noeud(0)] , [] , [] , [] , [] , [] ]


    """
    Cette fonction permet d'ajouter une adresse postale à l'automate.  Pour être ajouté à l'automate,
    l'adresse doit être valide.  La première chose consiste donc à la valider.  Ensuite on l'ajoute à
    l'endroit qui lui conrrespond.  À noter :
        -> La gestion des doublons se fait dans la classe Noeud.
        -> La gestion de la validité de l'adresse postale se fait dans la fonction 'validerFormatAdressePostale'.
    @param adressePostale   : Adresse postale qu'on veut ajouter à l'automate.
    @return                 : 'True si l'adresse est ajouté à l'automate.  'False' sinon.
    """
    def ajouterPossibilites(self, adressePostale):
        if not self.validerFormatAdressePostale(adressePostale):
            return False
        # On parcourt une deuxième fois l'adresse postale si elle est valide pour y ajouter les possibilités.
        for i in range(0, self.__nombreDeNoeuds):
            lettreAAjouter = adressePostale[i]
            if i is 0:
                self.__noeuds[i][0].ajouterPossibilite(lettreAAjouter)
            else:
                noeudReference = adressePostale[i - 1]
                noeudReferencePresent = False
                for noeud in self.__noeuds[i]:                          # On parcourt la possibilite des noeuds de reference.
                    if noeud.getNoeudReference() is noeudReference:     # Si on trouve le noeud de reference, 
                        noeud.ajouterPossibilite(lettreAAjouter)        # on ajoute le caractere a la liste de ses possibilités.
                        noeudReferencePresent = True
                        break
                if noeudReferencePresent is False:                      # Si on ne trouve pas le noeud de référence, on le rajoute.
                    nouveauNoeud = Noeud(noeudReference)                # On crée d'abord un nouveau Noeud avec le noeud de référence.
                    nouveauNoeud.ajouterPossibilite(lettreAAjouter)     # On ajoute ensuite la possibilité au nouveau Noeud.
                    self.__noeuds[i].append(nouveauNoeud)               # On ajout ce nouveau Noeud au tableau de l'automate.
        return True


    """
    Cette fonction permet de valider le format de l'adresse postale.
    Une adresse postale est invalide si elle :
        -> ne contient pas 6 caractères.
        -> ne respecte pas le format d'une adresse postale (fonction 'validerFormatCaractere').
    @param adressePostale   : Adresse qu'on veut valider.
    @return                 : 'True' si l'adresse est valide. 'False' sinon.
    """
    def validerFormatAdressePostale(self, adressePostale):
        if len(adressePostale) is not self.__nombreDeNoeuds:        # Si l'adresse postale ne contient pas 6 caractères, on quitte la fonction.
            print("L'adresse postale ", adressePostale, " est invalide. Elle ne contient pas assez de caractères.")
            return False
        # On parcourt une première fois l'adresse postale pour valider son format.
        for i in range (0 , self.__nombreDeNoeuds):
            lettreAAjouter = adressePostale[i]
            estIndicePaire = i % 2 == 0
            # Aux positions [0] , [2] et [4] de adressePostale, on doit retrouver une lettre.
            if estIndicePaire and not self.validerFormatCaractere(True, lettreAAjouter):
                print("L'adresse postale ", adressePostale, " est invalide. Elle n'a pas le bon format.")
                return False
            # Aux positions [1] , [3] et [5] de adressePostale, on doit retrouver un chiffre.
            elif not estIndicePaire and not self.validerFormatCaractere(False, lettreAAjouter):
                print("L'adresse postale ", adressePostale, " est invalide. Elle n'a pas le bon format.")
                return False
        return True


    """
    Fonction qui permet de valider si le 'caractere' est une lettre ou chiffre selon ce que spécifie
    le paramètre 'estUneLettre'.
    À noter pour cette fonction :
        -> isalpha() permet de dire si la chaine de caractères contient des caractères
           alphabétiques uniquement.
        -> isdigit() permet de dire si la chaine de caractères contient des chiffres uniquement.
    @param estUneLettre : Spécifie si le caractère doit être une lettre ou un chiffre.
    @param caractere    : Le caractère qu'on veut valider.
    @return             : 'True' si le format du caractère est valide. 'False' sinon.
    """
    def validerFormatCaractere(self, estUneLettre, caractere):
        return ( estUneLettre and caractere.isalpha() ) or ( not estUneLettre and caractere.isdigit() )


    """
    Fonction qui permet de savoir si une adresse postal se trouve dans la
    liste d'adresses postales valides.
    @param adressePostale   : L'adresse pour laquelle on veut savoir si elle se trouve dans l'automate.
    @return                 : 'True' si l'adresse postale se trouve dans l'automate.
    """
    def contientAdressePostale(self, adressePostale):
        if not self.validerFormatAdressePostale(adressePostale):
            return False                                        # Retourne 'False' si l'adresse postale n'est pas valide.
        for i in range (0 , self.__nombreDeNoeuds):             # Parcourt des noeuds.
            caractereAVerifier = adressePostale[i]
            if i == 0:                                          
                if not self.__noeuds[0][0].containsPossibilite(caractereAVerifier):
                    return False
            else:
                caractereReference = adressePostale[i - 1]
                for noeud in self.__noeuds[i]:                  # Parcourt des possibilités pour chaque noeud.
                    if noeud.getNoeudReference() == caractereReference:
                        if not noeud.containsPossibilite(caractereAVerifier):
                            return False
        return True


    """
    Fonction pour afficher les couches de noeuds se trouvant dans l'attribut '__noeuds' .
    """
    def afficherPossibilites(self):
        print()
        for i in range (0, 6):
            print("===== NIVEAU ", i, " =====")
            for noeudsPossibles in self.__noeuds[i]:
                noeudsPossibles.afficherNoeud()
            print()
        print()
            




