from CreationArbreAdresses import *
import sys


"""
    Cette fonction permet de traiter les requêtes en lisant un fichier texte
	contenant les requêtes. Apès la lecture du fichier, cette fonction valide
	les adresses en vérifiant si elles sont contenues dans l'automate.
	À noter:
		-­> La lecture du fichier se fait dans le fichier LectureFichier.py
		-> La validation de la requête se fait dans le fichier Automate.py
	La variable 'requetes' est un tableau de requêtes. Chaque requête est composée de la façon suivante :
		-> [0] : Adresse postale de départ.
		-> [1] : Adresse postale d'arrivée.
		-> [2] : Poids du colis.
    @param nomFichier   			: Nom du fichier contenant les requêtes à traiter.
	@param arbre					: Contient l'automate créé précédemment.
	@return requetes				: Tableau contenant toutes les requêtes valides du fichier texte.
	@return cptRequetesInvalides 	: Nombre de requêtes invalides contenue dans le fichier texte.
	@return cptRequetes				: Nombre de requêtes totales contenues dans le fichier texte.
"""
def traiterLesRequetes(nomFichier, arbre):
    # Lecture du fichier texte pour en retirer les requêtes.
	requetes = lectureFichierRequete(nomFichier)
	
	# Déclaration et initialisation de variables locales.
	tailleTableauRequetes = len(requetes)
	i = 0
	cptRequetes = 0
	cptRequetesInvalides = 0

	while i < tailleTableauRequetes and tailleTableauRequetes > 0:	# Boucle principale de la fonction.
		cptRequetes += 1											# Incrémentation du nombre de requêtes faites.

		# On vérifie qu'il y a bien des informations pour chaque portion de la requête.
		if len(requetes[i]) < 3 or requetes[i][0] == 'NULL' or requetes[i][1] == 'NULL' or requetes[i][2] is 'NULL':
			requetes.remove(requetes[i])			# S'il y une données erronées, on supprime la requête du tableau.
			tailleTableauRequetes = len(requetes)	# MAJ de la taille du tableau de requêtes.
			cptRequetesInvalides += 1				# Incrémentation du nombre de requêtes invalides.
			continue								# Retourne directement à l'instruction 'while' plus haut.
		
		# Informations sur la requête.
		adresseDepart = requetes[i][0]
		adresseArrivee = requetes[i][1]
		poids = int(requetes[i][2])

		# Affichage de la requête.
		print("\n\nDEMANDE DE REQUÊTE #", cptRequetes)
		print("\tAdresse de départ :\t", adresseDepart)
		print("\tAdresse d'arrivée :\t", adresseArrivee)
		print("\tPoids :\t\t\t", poids)
		
		# S'assurer que le poids est entre 0 et 5000g.
		if poids <= 0 or poids > 5000:
			print("* ATTENTION * Poids invalide pour cette requête. Elle est abandonnée. *")
			requetes.remove(requetes[i])			# S'il y une données erronées, on supprime la requête du tableau.
			tailleTableauRequetes = len(requetes)	# MAJ de la taille du tableau de requêtes.
			cptRequetesInvalides += 1				# Incrémentation du nombre de requêtes invalides.
			continue								# Retourne directement à l'instruction 'while' plus haut.


		# Vérification de la présence des adresses dans l'automate.
		contientAdresseDepart = arbre.contientAdressePostale(adresseDepart)
		contientAdresseArrivee = arbre.contientAdressePostale(adresseArrivee)
		# Si l'adresse n'est pas contenue dans l'automate, on refuse la requête.
		if contientAdresseDepart is False or contientAdresseArrivee is False:
			print("* ATTENTION * Une adresse est invalide ou n'existe pas pour cette requête. Elle est abandonnée. *")
			requetes.remove(requetes[i])			# On supprime la requête du tableau de requêtes.
			tailleTableauRequetes = len(requetes)	# MAJ de la taille du tableau de requêtes.
			cptRequetesInvalides += 1				# Incrémentation du nombre de requêtes invalides.
			continue								# Retroune directement à l'instruction 'while' plus haut. 
		
		i += 1										# On avance d'une place dans le tableau de requêtes.

	return requetes, cptRequetesInvalides, cptRequetes
