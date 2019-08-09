# coding: utf-8

import sys
import calculs
from parse import *
from fonctionPolynomiale import *
from parsingOutils import *
from resolutions import *

if __name__ == "__main__":
    variables, fonctions, matrices = {}, {}, {}
    chaine = input()
    while chaine != 'exit':
        parse_objet, test = Parsing(chaine), 0
        if not parse_objet.liste or not parse_objet.var or not parse_objet.var[0]:
            chaine = input()
            continue
        if parse_objet.tmp_inconnus:
            test, parse_objet.liste = remplacer(parse_objet.liste, variables, fonctions, matrices, parse_objet.tmp_inconnus, parse_objet.var)
        if test == 0 and len(parse_objet.liste) > 0:
            nom = parse_objet.var
            liste = parse_objet.liste
            if nom != '?' and len(nom) == 2:
                if nom[0] in fonctions.keys():
                    liste = calcul_fragmente(liste, fonctions[nom[0]][0])
                    liste = simplifier_polynome(liste, fonctions[nom[0]][0])
                    liste = integrer_2_polynomes(fonctions[nom[0]][1], liste)
                    liste = simplifier_polynome(liste, fonctions[nom[0]][0])
                    resoudre(liste, fonctions[nom[0]][0])
                else:
                    if tester_polynome(liste, nom[1]):
                        print(simple_print(liste, nom[1]))
                        fonctions[nom[0]] = [nom[1], liste]
                    else:
                        liste = calcul_fragmente(liste, nom[1])
                        if not liste: continue
                        liste = simplifier_polynome(liste, nom[1])
                        if not liste: continue
                        fonctions[nom[0]] = [nom[1], liste]
                        liste = nettoyer_polynome(liste, nom[1])
                        print(affiche_polynome(liste, nom[1]))
            else:
                print("la liste = {}".format(liste))
                reel, imaginaire, mat = traitement_partie_calculatoire(liste)
                print("Nom = {}".format(type(nom))
                if nom != '?' or nom != ['?']:
                    if mat != 'null':
                        matrices[nom[0]] = mat
                    elif imaginaire != '0' and imaginaire != 'null':
                        variables[nom[0]] = reel + ' + ' + imaginaire + ' * i'
                    elif reel != 'null':
                        variables[nom[0]] = reel
                    else:
                        pass
                if mat != 'null' and isinstance(mat, list) and len(mat) > 0:
                    print(matrice.affiche_matrice(mat))
                elif imaginaire != '0' and imaginaire != 'null':
                    if reel != '0':
                        char = ' + '
                        if calculs.nombre(imaginaire) < 0 :
                            imaginaire = imaginaire[1:]
                            char = ' - '
                        if imaginaire != '1': 
                            print('{}{}{}i'.format(reel, char, imaginaire))
                        else:
                            print('{}{}i'.format(reel, char))
                    else:
                        print('{}i'.format(imaginaire))
                elif reel != 0 and reel != 'null':
                    print(reel)
                else:
                    pass
            print("var matrices = {}".format(matrices))
        chaine = input()