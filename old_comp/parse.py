# coding: utf-8

import re
import parsingOutils as outils
import fonctionPolynomiale as polynome

class Parsing:
    """ Parser la chaine.
    1- verifier l'existence d'un seul = dans la chaine
    2- spliter la chaine en deux parties : droite et gauche
    3- Si la partie droite est '?', il s'agit d'evaluer la partie gauche
    4- Sinon la partie gauche est le nom de variable à stocker dans un dictionnaire avec la valeur."""

    def __init__(self, chaine):

        liste_gauche, liste_droite = outils.equal_number(chaine)
        self.var, self.liste, self.tmp_inconnus = [], [], {}
        # permutation des parties gauche et droite dans le cas ou la partie droite = '?'
        if liste_droite and liste_gauche:
            liste_droite = liste_droite.strip()
            liste_gauche = liste_gauche.strip()
            if re.match(r'( )?\?( )?', liste_droite):
                liste_droite = liste_gauche
                liste_gauche = '?'
            # traiter la partie gauche
            self.var = outils.traitement_nom_de_variable(liste_gauche)
            # traiter la partie droite
            if '[' in liste_droite:
                self.liste, self.tmp_inconnus = outils.traitement_matrice(liste_droite)
            else:
                self.liste, self.tmp_inconnus = outils.test_partie_calculatoire(liste_droite, self.var)