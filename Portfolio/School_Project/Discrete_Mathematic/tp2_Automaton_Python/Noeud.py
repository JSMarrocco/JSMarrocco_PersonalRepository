"""
Fonctions contenues par la classe Automate :
    -> getNoeudReference()
    -> getPossibilites()
    -> getPossibilite(index)
    -> getNbPossibilites()
    -> containsPossibilite(possibilite)
    -> ajouterPossibilite(possibilite)
    -> afficherNoeud()
"""

class Noeud():
    
    """
    Constructeur par paramètre.  Initialisation des attributs de la classe.
    @param noeudReference   : Noeud de référence (précédent) du noeud courant.
    """
    def __init__(self, noeudReference):
        self.__noeudReference = noeudReference
        self.__possibilites = []


    """
    Accesseur pour l'attribut __noeudReference.
    @return : L'attriut __noeudReference.
    """
    def getNoeudReference(self):
        return self.__noeudReference


    """
    Accesseur pour l'attribut __possibilites.
    @return : L'attribut __possibilites.
    """
    def getPossibilites(self):
        return self.__possibilites


    """
    Permet d'obtenir la possibilité à un indice spécéfié en paramètre.
    @param index    : L'indice à lequel on veut obtenir la possibilité.
    @return         : La possibilité à l'indice passé en paramètre.
    """
    def getPossibilite(self, index):
        if index < len(self.__possibilites) and index >= 0:
            return self.__possibilites[index]
        else:
            return None
    

    """
    Retourne le nombre de possibilités pour le noeud courant.
    @return         : Le nombre de possibilités pour le noeud.
    """
    def getNbPossibilites(self):
        return len(self.__possibilites)


    """
    Indique si la possibilite passée en paramètre se retrouve dans l'automate.
    @param possibilite  : Une possibilité pouvant être contenue dans l'automate.
    @return             : 'True' si la possiblité est dans l'automate. 'False' sinon.
    """
    def containsPossibilite(self, possibilite):
        for poss in self.__possibilites:
            if possibilite == poss:
                return True
        return False


    """
    Permet d'ajouter une possibilité à l'automate. La fonction vérifie d'abord
    si la possibilité ne se retrouve pas déjà dans l'automate.
    @param possibilite  : Une possibilité pouvant être contenue dans l'automate.
    """
    def ajouterPossibilite(self, possibilite):
        if not self.containsPossibilite(possibilite):
            self.__possibilites.append(possibilite)


    """
    Affiche dans le terminal une représentation du noeud courant. Affiche d'abord
    le noeud de référence, et ensuite toutes les possibilités pour notre noeud.
    """
    def afficherNoeud(self):
        print("Noeud reference : ", self.__noeudReference, end="")
        print("\tPossibilités : " , end="")
        for possibilite in self.__possibilites:
            print(possibilite, " , ", end="")
        print()

    