#include <iostream>
#include <string>

#include "LecteurFichier.h"

// Prototypage
void creerGrapheOriente(std::string pNomFichier);
void genererHasse(std::string pNomFichier);

int main()
{
	// Changer ceci selon le nom du fichier
	std::string nomDuFichier("manger.txt");
	std::string choix;

	while (choix != "c") {
		std::cout <<std::endl<< std::endl << "*********  MENU PRINCIPAL RECETTES  *********" << std::endl << std::endl << std::endl;
		std::cout << "(a) Creer et afficher le graphe des recettes." << std::endl << std::endl;
		std::cout << "(b) Generer et afficher le diagramme de Hasse." << std::endl << std::endl;
		std::cout << "(c) Quitter." << std::endl << std::endl;
		std::cout << "Choix: ";
		std::cin >> choix;
		std::cout << std::endl;

		if (choix == "a" || choix == "A")
			creerGrapheOriente(nomDuFichier);
		else if (choix == "b" || choix == "B")
			genererHasse(nomDuFichier);
		else if (choix == "c" || choix == "C")
			break;
		else
			std::cout << std::endl << "Choix invalide." << std::endl << std::endl;
	}

	std::cout << std::endl << "Au revoir." << std::endl;
	return 0;
}

void creerGrapheOriente(std::string pNomFichier) {
	LecteurFichier fichier;
	fichier.lireFichier(pNomFichier);
	std::vector<std::pair<int, std::string>> vecSommets = fichier.getSommets();
	std::vector<std::pair<int, int>> vecAretes = fichier.getAretes();

	// Affichage du graphe.
	for (size_t i = 0; i < vecSommets.size(); ++i) {
		std::cout << "(" << vecSommets[i].second << "," << vecSommets[i].first << ",";
		for (size_t j = 0; j < vecAretes.size(); ++j) {
			if (vecAretes[j].second == vecSommets[i].first)
				std::cout << "(" << vecSommets[(vecAretes[j].first)-1].second << ")" << ",";
			if (vecAretes[j].first == vecSommets[i].first)
				std::cout << "(" << vecSommets[(vecAretes[j].second)-1].second << ")" << ",";
		}
		std::cout << ")" << std::endl;
	}
}


void genererHasse(std::string pNomFichier)
{
	LecteurFichier fichier;
	fichier.lireFichier(pNomFichier);
	std::vector<std::pair<int, std::string>> vecSommets = fichier.getSommets();
	std::vector<std::pair<int, int>> vecAretes = fichier.getAretes();

	// Affichage.
	for (size_t i = 0; i < vecSommets.size(); ++i) {
		std::cout << std::endl<<"liste" << i + 1 << ":" << vecSommets[i].second;
		for (size_t j = 0; j < vecAretes.size(); ++j) {
			if (vecAretes[j].first == vecSommets[i].first) {
				std::cout << "--->" << vecSommets[(vecAretes[j].second) - 1].second;
				for (size_t k = 0; k < vecAretes.size(); ++k) {
					if (vecAretes[k].first == vecAretes[j].second)
						std::cout <<"--->" << vecSommets[(vecAretes[k].second) - 1].second;
				}
			}
			
		}
	}
}