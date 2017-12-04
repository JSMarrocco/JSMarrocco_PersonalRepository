#pragma once

#include <string>
#include <vector>
#include <utility>

class LecteurFichier
{
public:
	// Lis le fichier et remplit les vecteurs.
	void lireFichier(std::string pNomFichier);

	// Retourne la liste des sommets sous la forme <id, étiquette>.
	std::vector<std::pair<int, std::string>> getSommets() { return m_sommets; }

	// Retourne la liste des aretes sous la forme <sommet1, sommet2>.
	std::vector<std::pair<int, int>> getAretes() { return m_aretes; }

private:
	std::vector<std::pair<int, std::string>> m_sommets;
	std::vector<std::pair<int, int>> m_aretes;
};

