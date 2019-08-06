# coding: utf-8

import re
import matrice
from test_nom_de_variable import *
import fonctionPolynomiale as polynome
import calculs
import complexe
from copy import deepcopy

def remplacer(liste, tmp_var, tmp_fonction, tmp_matrices, tmp_inconnus, var):
# chercher les variables inconnues et les remplacer par leur valeurs

    inconnu = '0'
    if len(var) == 2:
        inconnu = var[1]
    for key, element in tmp_inconnus.items():
        if isinstance(element, dict):
            cle = list(tmp_inconnus.keys())[list(tmp_inconnus.values()).index(element)]
            test, liste[cle] = remplacer(liste[cle], tmp_var, tmp_fonction, tmp_matrices, element, var)
            if test == 0 and len(liste) > 0:
                continue
            return test, liste
        if isinstance(element, list):
            valeur = element[1][0]
            fonction = element[0]
            if fonction in ['det', 'inv', 'com', 'trans']:
                if tmp_matrices and valeur.lower() in tmp_matrices:
                    element[1][0] = tmp_matrices[valeur.lower()]
                    continue
                else:
                    print("Error : matrix not defined")
                    return -1, []
            if ((len(tmp_var.keys()) > 0 and valeur.lower() not in tmp_var.keys() and not re.match(r'^[0-9]+(\.[0-9]+)?$', valeur)) \
                or (len(tmp_fonction) > 0 and fonction.lower() not in tmp_fonction.keys())):
                print("Error : variable or function not defined")
                return -1, []
            if valeur.lower() in tmp_var.keys():
                valeur = tmp_var[valeur.lower()]
            inconnu = tmp_fonction[fonction.lower()][0]
            fonction = deepcopy(tmp_fonction[fonction.lower()][1:])
            liste[key] = polynome.calcul(fonction, valeur, inconnu)
            liste[key + 1] = 'null'
        elif tmp_var and element.lower() in tmp_var.keys():
            liste_inter = liste[:key]
            liste_inter += tmp_var[element.lower()].split()
            liste_inter += liste[key + 1:]
            liste = liste_inter
        elif tmp_matrices and element.lower() in tmp_matrices.keys():
            liste_inter = liste[:key]
            liste_inter += [deepcopy(tmp_matrices[element.lower()])]
            liste_inter += liste[key + 1:]
            liste = liste_inter
        elif element == inconnu:
            continue
        else:
            print("Error : variable not defined")
            return -1, []
    liste = nettoyer_post_remplacement(liste)
    return 0, liste

# tester si la fonction est polynomiale ou pas
def tester_polynome(liste, inconnu):

    index = 0
    while index < len(liste):
        if liste[index] == '/':
            if liste[index - 1] == inconnu or liste[index + 1] == inconnu or (isinstance(liste[index + 1], list) and inconnu in liste[index + 1]):
                return 1
        index += 1
    return 0

# nettoyer la liste apres leremplacement
def nettoyer_post_remplacement(liste):

    index = 0
    while index < len(liste):
        if liste[index] == 'null':
            del liste[index]
        else:
            index += 1
    return liste

# verifier l'existence d'un seul = dans la chaine
def equal_number(chaine):

    liste = chaine.split('=')
    try:
        assert len(liste) == 2 and liste[0] != '' and liste[1] != ''
    except:
        print('Error : we must have an expression like a = b + c or b + c = ?')
        return '', ''
    else:
        return liste[0], liste[1]

# trouver l'indice de du caractere fermant char2
def indice_caractere(chaine, char1, char2):

    i = 0
    nbr_caractere_ouvrant = 1
    longueur = len(chaine)
    while i < longueur:
        if chaine[i] == char1:
            nbr_caractere_ouvrant += 1
        if chaine[i] == char2:
            nbr_caractere_ouvrant -= 1
        if nbr_caractere_ouvrant == 0:
            break
        i += 1
    try:
        assert nbr_caractere_ouvrant == 0 or i < longueur and chaine[i] == char2
        if nbr_caractere_ouvrant == 0:
            return i
        while i < longueur:
            if chaine[i] == char2:
                if nbr_caractere_ouvrant == 0:
                    return i
                else:
                    nbr_caractere_ouvrant -= 1
            i += 1
        print('Error : brackets\' problem')
        return -1
    except AssertionError:
        print('Error : brackets\' problem')
        return -1

# transfomer une partie de la chaine de caractere principale en une liste
def test_elementaire(chaine):

    liste_finale = []
    liste = chaine.split()
    print("liste apres split = {}".format(liste))
    for i, element in enumerate(liste):
        print("element = {}".format(element))
        if element == ')':
            return liste_finale
        m = re.search(r"(\*|-|%|/|\+|\^)", element)
        if element in '+*-/%^':
            liste_finale.append(element)
        elif m:
            char = m.group(0)
            liste_intermediaire = element.split(char)
            print("liste_intermediare = {}".format(liste_intermediaire))
            # if liste_intermediaire[0] == '':
                # liste_finale.append(element)
            #   liste_intermediaire = liste_intermediaire[1:]
            #else:
            for key, el in enumerate(liste_intermediaire):
                if el != '':
                    liste_finale.append(el)
                if key < len(liste_intermediaire) - 1 or (element[len(element) - 1] in '+*-/%^' and i < len(element) - 1):
                    liste_finale.append(char)
            print("liste_finale apres append = {}".format(liste_finale))
        else:
            liste_finale.append(element)
    return liste_finale

# transfomer une chaine de caractere en une liste.
def premier_test(chaine):

    liste_finale = []
    if '(' not in chaine:
        print("chaine test elementaire = {}".format(chaine))
        return test_elementaire(chaine)
    else:
        indice_1 = chaine.index('(')
        if indice_1 != 0:
            liste_finale = liste_finale + test_elementaire(chaine[:indice_1].strip())
            print("la liste finale_indice != 0= {}".format(liste_finale))
        indice_1 += 1
        nouvelle_chaine = chaine[indice_1:].strip()
        print("nouvelle chaine_indice_1 = {}".format(nouvelle_chaine))
        indice_2 = indice_caractere(nouvelle_chaine, '(', ')')
        if indice_2 > 0:
            print("liste fianle avant append 1 = {}".format(liste_finale))
            liste_finale.append(premier_test(nouvelle_chaine[:indice_2].strip()))
            print("la liste finale apres 1 = {}".format(liste_finale))
            indice_2 += 1
            if indice_2 < len(nouvelle_chaine):
                print("2")
                liste_finale = liste_finale + premier_test(nouvelle_chaine[indice_2:].strip())
        else:
            liste_finale.append([])
    return liste_finale

# traiter le nom de la variable ou de fonction
def traitement_nom_de_variable(chaine):

    if chaine == '?':
        return [chaine]
    # test de la variable avec 'i'
    if not test_complexe(chaine):
        return []
    if '(' in chaine or ')' in chaine:
        # recuperer dans ce cas le nom de la fonction, de la composition s'il y en a et le nom de l'inconu
        fonction, inconnu = test_fonction(chaine)
        return [fonction.lower(), inconnu.lower()]
    else:
        # tester le nom de la variable
        if test_variable(chaine) == 1:
            return [chaine.lower()]
        return []

#  organiser la chaine : chaque element est dans un bloc
def organiser_chaine(chaine):

    if len(chaine) == 1:
        return [chaine]
    if re.match(r'^[0-9]+(\.[0-9]+)?|[a-zA-Z]+$', chaine):
        return [chaine]
    liste_finale = []
    m = re.search(r'(\*|\^|\/|%|\+|-|i|[a-zA-Z]+)', chaine)
    if not m:
        return []
    char = m.group(0)
    liste_inter = chaine.split(char)
    for element_inter in liste_inter:
        if element_inter == '':
            continue
        if re.match(r'^([0-9]+|[a-zA-Z]+|i)$', element_inter):
            liste_finale.append(element_inter)
        else:
            liste_finale.extend(organiser_chaine(element_inter))
        if char == 'i' or re.match('[a-zA-Z]+', char):
            liste_finale.append('*')
            liste_finale.append(char)
        elif liste_inter.index(element_inter) != len(liste_inter) - 1:
            liste_finale.append(char)
        else:
            pass
    return liste_finale

#  organiser la nouvelle liste pour mieux faire le calcul
def organiser_liste(liste):

    liste_finale = []
    for element in liste:
        if isinstance(element, list):
            liste_finale.append(organiser_liste(element))
        elif re.match(r'^(([0-9]+(\.[0-9]+)?)|\*|\*\*|\^|\/|%|\+|-|i|[a-zA-Z]+)$', element):
            liste_finale.append(element)
        elif re.match(r'^(-[a-zA-Z]+)$', element):
            liste_finale.extend(['-1', '*', element[1:]])
        elif re.match(r'^(-[0-9]+(\.[0-9]+)?)$', element):
            if element == liste[0]:
                liste_finale.append(element)
            else:
                liste_finale.extend(['-', element[1:]])
        elif re.match(r"^(-)?(\+)?[0-9]+(\.[0-9]+)?[a-zA-Z]+$", element):
            m = re.search(r"(-)?[0-9]+(\.[0-9]+)?", element)
            nombre = m.group(0)
            m = re.search(r"[a-zA-Z]+", element)
            var = m.group(0)
            if len(liste_finale) != 0 and liste_finale[len(liste_finale) - 1] not in '+-/*':
                liste_finale.append('+')
            liste_finale.extend([nombre, '*', var])
        else:
            while element:
                m = re.search(r"\*|\/|\+|-|%|\^", element)
                if m:
                    char = m.group(0)
                    if char == element:
                        print ("Error Operator")
                        return []
                    index_char = element.index(char)
                    if index_char != 0:
                        liste_finale.append(''.join(element[:index_char]))
                    liste_finale.append(element[index_char])
                    if index_char != len(element) - 1:
                        element = ''.join(element[index_char + 1:])
                else:
                    if element != 'i':
                        liste_inter = organiser_chaine(element)
                        if not liste_inter:
                            print("Error : Syntax")
                            return []
                        liste_finale.extend(liste_inter)
                    else:
                        liste_finale.append('i')
                    element = ''
    return liste_finale

# tester la partie calculatoire
def test_partie_calculatoire(chaine, nom_var):

    inconnu = ''
    if len(nom_var) == 2:
        inconnu = nom_var[1]
    # parsing pour mettre cette expression dans une liste
    print("la liste avant premier test = {}".format(chaine))
    liste = premier_test(chaine)
    print("la liste apres premier test = {}".format(liste))
    # eliminer les elements vides
    for element in liste:
        if not element:
            liste.remove(element)
    # chaque nombre et operateur constitue un element tout seul de la liste
    liste = organiser_liste(liste)
    if not liste or len(liste) == 0:
        return liste, {}
    # chercher les variables inconnues et se trouvant dans l'expression
    variables = calculs.variables_inconnues(liste)
    return liste, variables

# traiter la partie calculatoire
def traitement_partie_calculatoire(liste):
    # traiter la partie calculatoire

    reel, img, mat = '0', '0', 'null'
    # aucune trace de matrice, pas de complexe
    # complexe
    struct = calculs.verifier_structure(liste)
    if struct == 1:
        img, reel, liste = complexe.calcul_imaginaire(liste)
        if len(liste) > 0:
            if liste[0] == '+':
                liste = liste[1:]
            if liste[0] == '-':
                liste = liste[1:]
                liste[0] = '-' + liste[0]
            reel = calculs.nombre(calculs.calcul_global(liste)) + calculs.nombre(reel)
        reel = str(reel)
    elif struct == 2:
        mat = matrice.traiter(liste)
    else:
        reel = calculs.calcul_global(liste)
    return reel, img, mat

# traiter une chaine de liaison entre deux matrices
def traitement_liaison(chaine):

    liste = []
    for element in chaine:
        m = re.search(r'\*|\+|\/|-|%', chaine)
        char = m.group(0)
        index = chaine.index(char)
        if index != 0:
            liste.append(chaine[:index].strip())
        liste.append(char)
        chaine = chaine[index + 1:].strip()
    if chaine:
        liste.append(chaine)
    return liste

# traiter les matrices possibles
def traitement_matrice(chaine):

    liste = []
    inconnus = {}
    while '[' in chaine:
        index = chaine.index('[')
        fin = indice_caractere(chaine[index + 1:].strip(), '[', ']') + index
        if fin < 0:
            return [], []
        if index != 0:
            liste_avant = chaine[:index].strip().split()
            inconnus.update(calculs.variables_inconnues(liste_avant))
            liste.extend(liste_avant)
        matrice_element = matrice.matrice_parsing(chaine[index + 1:fin + 1].strip())
        if not matrice_element:
            return [], []
        liste.append(matrice_element)
        if fin < len(chaine) - 1:
            chaine = chaine[fin + 2:].strip()
    if chaine != '' and chaine != ' ':
        liste.extend(chaine.split())
    return liste, inconnus