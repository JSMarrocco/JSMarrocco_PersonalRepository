class Drone(object):
    def __init__(self, type):                       # Constructeur.
       self.type_ = type
       self.batterie_ = 100
    
    # Méthode permet de changer le type de drone utilisé.
    def setType(self,type):
        self.type_ = type

    # Méthode pour calculer le pourcentage restant de batterie.
    def utiliserBatterie(self,typeColis, temps):
        utilisationPile = 0
        if(self.type_ == "3.3"):
            if(typeColis == "plume"):
                utilisationPile = (temps / 10) * 10 # -10% -> 10min
            elif(typeColis == "moyen"):
                utilisationPile = (temps / 10) * 20 # -20% -> 10min
            elif(typeColis == "lourd"):
                utilisationPile = (temps / 10) * 40 # -40% -> 10min
        if(self.type_ == "5.0"):
            if(typeColis == "plume"):
                utilisationPile = (temps / 10) * 10 # -10% -> 10min
            elif(typeColis == "moyen"):
                utilisationPile = (temps / 10) * 15 # -15% -> 10min
            elif(typeColis == "lourd"):
                utilisationPile = (temps / 10) * 25 # -25% -> 10min
        self.batterie_ -= utilisationPile