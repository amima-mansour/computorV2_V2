# coding: utf-8

import calculs
import fonctionPolynomiale as polynome

# fonction qui permet de retrouver a, b, c et le discriminant tel que a * x^2 + b * x + c = 0
def parametre_equation(liste, inconnu):

    liste_finale = []
    a, b, c, index = 0, 0, 0, 0
    index = 0
    print("la liste parametre = {}".format(liste))
    while index < len(liste):
        print("la liste a traiter = {}".format(liste))
        if isinstance(liste[index], list):
            coeff = 1
            if index - 1 >= 0 and liste[index - 1] == '-':
                coeff *= -1
            if index - 2 >= 0 and liste[index - 1] == '*':
                coeff *= calculs.nombre(liste[index - 2])
                if index - 3 >= 0 and liste[index - 3] == '-':
                    coeff *= -1
            if index + 1 < len(liste) and liste[index + 1] == '^':
                liste[index] = polynome.developper_puissance(liste[index], inconnu, calculs.nombre(liste[index + 2]))
                del liste[index + 1:index + 3]
                print("liste apres developpement = {}".format(liste))
            a_tmp, b_tmp, c_tmp = parametre_equation(liste[index], inconnu)
            a += coeff * a_tmp
            b += coeff * b_tmp
            c += coeff * c_tmp
        if liste[index] == inconnu:
            coeff = 1
            if index - 3 >= 0 and liste[index - 3] == '-':
                coeff *= -1
            if liste[index + 2] == '0':
                c += coeff * calculs.nombre(liste[index - 2])
            elif liste[index + 2] == '1':
                b += coeff * calculs.nombre(liste[index - 2])
            else:
                a += coeff * calculs.nombre(liste[index - 2])
        index += 1
    return a, b, c

# trouver le degree
def degree_polynome(liste, inconnu):

    degree = 0
    index = 0
    while index < len(liste):
        if isinstance(liste[index], list):
            degree_1 = degree_polynome(liste[index], inconnu)
            if index + 2 < len(liste) and liste[index + 1] == '^':
                degree_1 *= calculs.nombre(liste[index + 2])
                index += 2
            if degree < degree_1: degree = degree_1
            index += 1
            continue
        if liste[index] == '^':
            nbr = calculs.nombre(liste[index + 1])
            if degree < nbr and calculs.nombre(liste[index - 3]) != 0: degree = nbr
            index += 2
        else:
            index += 1
    return degree

# resolution
def resoudre(liste, inconnu):

    a, b, c = parametre_equation(liste, inconnu)
    print("a = {}, b = {}, c = {}".format(a, b, c))
    d = degree_polynome(liste, inconnu)
    if d == 0:
        print("The solution is:\nAll real numbers")
    elif d == -1:
        print("The solution is:\nNo possible solution")
    elif d > 2:
        print("The polynomial degree is stricly greater than 2, I can't solve.")
    else:
        if d == 1:
            solution = -1 * c / b
            if type(solution) == float:
                solution = round(solution, 6)
            print("The solution is:\n{}".format(solution))
        else:
            solutions(a, b, c)

def racine_carre(nombre):
    # Cette fonction calcule la racine carree d'un nombre

    i = 0.000001
    while i * i < nombre:
        resultat = i
        i += 0.000001
    return resultat

def solutions(a, b, c):
    # Cette fonction trouve les solutions d'une equation de second degree.

    discriminant = b * b - 4 * a * c
    if discriminant == 0:
        solution = -1 * b / (2 * a)
        if type(solution) == float:
            solution = round(solution, 6)
        print ("Discriminant is null, the solution is:\n{}".format(solution))
    elif discriminant > 0:
        racine = racine_carre(discriminant)
        solution_1 = (-1 * b + racine) / (2  * a)
        solution_2 = (-1 * b - racine) / (2  * a)
        if type(solution_1) == float:
            solution_1 = round(solution_1, 6)
        if type(solution_2) == float:
            solution_2 = round(solution_2, 6)
        print("Discriminant is strictly positive, the two solutions are:\n{}\n{}".format(solution_2, solution_1))
    else:
        racine = racine_carre(-1 * discriminant)
        premiere_partie = -1 * b / (2 * a)
        seconde_partie =  racine / (2  * a)
        if type(premiere_partie) == float:
            premiere_partie = round(premiere_partie, 6)
        if type(seconde_partie) == float:
            seconde_partie = round(seconde_partie, 6)
        print("Discriminant is strictly negative, the two solutions are:\n{} - i * {}\n{} + i * {}".format(premiere_partie,
            seconde_partie, premiere_partie, seconde_partie))
