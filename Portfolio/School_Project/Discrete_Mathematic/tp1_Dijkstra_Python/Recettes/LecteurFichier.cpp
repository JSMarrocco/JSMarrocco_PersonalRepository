#include "LecteurFichier.h"

#include <fstream>
#include <iostream>

void LecteurFichier::lireFichier(std::string pNomFichier)
{
	std::ifstream fichier(pNomFichier);
	std::string ligne;

	if (fichier.is_open()) {
		// Sommets
		while (!fichier.eof()) {
			getline(fichier, ligne);

			if (ligne.empty()) {									// Si la ligne est vide, on passe aux aretes.
				break;

			int pos = ligne.find(',');								// Position de la virgule.
			int id = std::stoi(ligne.substr(0, pos));				// Numéro du sommet.
			std::string nom = ligne.substr(pos + 1, ligne.size());	// Nom du sommet.
			m_sommets.push_back(std::make_pair(id, nom));
			}
		}

		// Aretes
		while (!fichier.eof()) {
			getline(fichier, ligne);

			if (ligne.empty())											// Si la ligne est vide, on a fini.
				break;

			int pos = ligne.find(',');									// Position de la virgule.
			int id1 = std::stoi(ligne.substr(0, pos));					// Numéro du sommet 1.
			int id2 = std::stoi(ligne.substr(pos + 1, ligne.size()));	// Numero du sommet 2.
			m_aretes.push_back(std::make_pair(id1, id2));
		}
	}
	else
		std::cout << "Erreur de fichier." << std::endl;
}