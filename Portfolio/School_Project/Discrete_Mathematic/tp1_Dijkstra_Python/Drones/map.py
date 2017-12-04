from collections import defaultdict

# Classe pour les Sommets.
class Sommet(object):
    id_ = 0
    peuRecharger_ = False

    def __init__(self, id, peuRecharger):                   # Constructeur.
        self.id_ = id
        self.peuRecharger_ = peuRecharger
        self.visited = False

# Classe pour les Arcs.
class Arc(object):
    distance_ = 0
    entree_ = 0
    sortie_ = 0

    def __init__(self,entree, sortie, distance):            # Constructeur.
        self.entree_ = entree
        self.sortie_ = sortie
        self.distance_ = distance

# Classe pour le Graphe.
class Graphe(object): 
    def __init__(self):                                     # Constructeur.
        self.toggle = False
        self.noeuds = set()
        self.arcs = defaultdict(list)
        self.distances = {}
        self.nbrBorne = 0;
        
        self.listSommet = []  
        self.listArc = []
        self.map = []
        self.map.append([])

    def ajouterNoeud(self,valeur):
        self.noeuds.add(valeur)

    def ajouterArc(self, entree, sortie, distance):
        self.arcs[entree].append(sortie)
        self.arcs[sortie].append(entree)
        self.distances[(entree,sortie)] = distance
        self.distances[(sortie,entree)] = distance

    # Méthode pour créer le graphique.
    def creeGraphe(self, nomFichier):
        # Lit le fichier.
        with open(nomFichier,  "r") as f:
            # Lit chaque ligne.
            for line in f:
                data = line.split(',')                      # Split la line à chaque ',' .
                # Si la ligne est un espace vide.
                if not line.strip():
                    self.toggle = True
                    continue                                # Skip une interactions.
                if self.toggle == False:
                    self.listSommet.append(Sommet(data[0], int(data[1])))
                    self.ajouterNoeud(int(data[0]))
                    if int(data[1]) == 1:
                        self.nbrBorne+= 1
                else:
                    self.ajouterArc(int(data[0]),int(data[1]),int(data[2]))
                    self.listArc.append(Arc(data[0],data[1],data[2]))                
        self.creeMap()
    
    # Méthode pour créer la matrice du graphe.
    def creeMap(self):
        dimension = len(self.listSommet)
        self.map = [[0 for i in range(dimension)] for j in range(dimension)]
        for arc in self.listArc:
            indexEntree = int(arc.entree_) - 1
            indexSortie = int(arc.sortie_) - 1
            # Condition pour s'assurer que les dimension sont respectées.
            if (indexEntree < dimension and indexSortie < dimension ):
                self.map[indexEntree][indexSortie] = int(arc.distance_)
                self.map[indexSortie][indexEntree] = int(arc.distance_)

    # Méthode pour afficher le graphe en matrice d'incidence.
    def affichierGraphe(self):
        # Afficher le titre (numéro de sommets) des colonnes au haut de la matrice.
        print('\n=========== PRÉSENTATION MATRICIELLE ===========\n')
        print('       ', end="")
        for item in self.listSommet:
            print('{:4}'.format(item.id_), end="")
        print(' ')
        print('    ', end="")
        for item in self.listSommet:
            print('{:4}'.format("____"), end="")
        print(' ')
        # Afficher la  matrice.
        enum = 1
        for row in self.map:
            if enum < 10:
                print(enum,' |', end="")
            else:
                print(enum,'|', end="")
            enum +=1
            for val in row:
                 print('{:4}'.format(val), end="")
            print('  |', end="")
            print('')

    # Méthode qui affiche la matrice en format chaine de caractères.
    def afficherGraphiqueLigne(self):
        print('\n\n=========== PRÉSENTATION CHAINE DE CARACTÈRES ===========\n')
        numeroDeLigne = 1
        numColonne = 1
        for row in self.map:
            print('Le sommet ', numeroDeLigne, ' a les voisins suivants (voisins, distance) : ', end = "")
            for val in row:
                if val != 0:
                    print('(', numColonne, ',', val,') ' , end = "")
                numColonne += 1
            print('.')
            numeroDeLigne += 1
            numColonne = 1
        
        
            
            



           
           
            

