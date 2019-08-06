# coding: utf-8

import re
#from calculs import *
import calculs

def puissance_complexe(nbr):
    # puissance complexe

    test = True
    if nbr % 2 == 0:
        test = False
    return test, (-1) ** (nbr // 2)

def trouver_indice_fin(liste, start, pas):
    # renvoie l'indice de la partie a traiter

    fin = start
    if pas > 0:
        while fin < len(liste) and liste[fin] != '-' and liste[fin] != '+':
            fin += pas
        return fin
    while fin > -1 and liste[fin] != '-' and liste[fin] != '+':
        fin += pas
    return fin + 1

def calcul_elementaire_complexe(char, test):
    # Cette fonction permet de faire un calcul elementaire complexe.

    nbr = 1
    if (char == '*' and test) or (char == '\\' and not test):
        return -1
    if (char == '*' and not test) or (char == '\\' and test):
        return 1
    return 1

def calcul_complexe_elementaire_gauche(liste, start, char):
    # effectuer des calculs elementaires en respectant la priorite

    fin = trouver_indice_fin(liste, start, -1)
    liste_a_traiter = liste[fin:start]
    liste = liste[:fin] + liste[start + 1:]
    if len(liste_a_traiter) == 1:
        img = calculs.nombre(calculs.calcul_global([liste_a_traiter[0]]))
    else:
        img = calculs.nombre(calculs.calcul_global(liste_a_traiter))
    if char == '/':
        img *= -1
    return calculs.nombre(img), liste

def calcul_complexe_elementaire_droite(liste, start):
    # effectuer des calculs elementaires en respectant la priorite

    fin = trouver_indice_fin(liste, start, 1)
    liste_a_traiter = liste[start + 1:fin]
    char = liste[start]
    liste = liste[:start] + liste[fin:]
    test = True
    resultat = 1
    while 'i' in liste_a_traiter:
        index = liste_a_traiter.index('i')
        liste_a_traiter[index] = '1'
        if index == 0:
            resultat *= calcul_elementaire_complexe(char, test)
        else:
            resultat *= calcul_elementaire_complexe(liste_a_traiter[index - 1], test)
        test = not test
    nbr = resultat * calculs.nombre(calculs.calcul_global(liste_a_traiter))
    imag, reel = 0, 0
    if test:
        imag = nbr
    else:
        reel = nbr
    return imag, reel, liste

def calcul_toute_puissance_complexe(liste):
    # calcule tous les i^n

    if 'i' not in liste or '^' not in liste:
        return liste
    index = liste.index('i')
    for key, element in enumerate(liste):
        if element != 'i' or (key < len(liste) - 1 and liste[key + 1] != '^'):
            continue
        test, nbr = puissance_complexe(calculs.nombre(liste[key + 2]))
        liste[key + 1] = '*'
        liste[key + 2] = str(nbr)
        if not test:
            del liste[key]
            del liste[key]
    return liste

def calcul_toute_division_complexe(liste):
    # calcule tous les i / n

    if 'i' not in liste or '/' not in liste:
        return liste
    index = liste.index('i')
    for key, element in enumerate(liste):
        if element != 'i' or (key < len(liste) - 1 and liste[key + 1] != '/'):
            continue
        nbr = 1 / calculs.nombre(liste[key + 2])
        liste[key + 1] = '*'
        liste[key + 2] = str(nbr)
    return liste


def calcul_imaginaire(liste):
    # retourner la partie imaginaire dans l'expression

    liste = calcul_toute_puissance_complexe(liste)
    liste = calcul_toute_division_complexe(liste)
    img_total, reel_total = 0, 0
    while 'i' in liste:
        index = liste.index('i')
        img_droite, img_gauche, reel_droite = 1, 1, 1
        if index != 0 and (liste[index - 1] == '*' or liste[index - 1] == '/'):
            char = liste[index - 1]
            img_gauche, liste = calcul_complexe_elementaire_gauche(liste, index - 1, char)
        index = liste.index('i')
        if index < len(liste) - 1 and liste[index + 1] == '*':
            img_droite, reel_droite, liste = calcul_complexe_elementaire_droite(liste, index + 1)
        img,reel = 0, 0
        if img_droite != 0 and img_gauche != 0:
            img = img_droite * img_gauche
        else:
            reel = reel_droite * img_gauche
        index = liste.index('i')
        if index != 0 and liste[index - 1] in '-+':
            if liste[index - 1]  == '-':
                img *= -1
                reel *= -1
            del liste[index - 1]
            del liste[index - 1]
        else:
            del liste[index]
        img_total += img
        reel_total += reel
    return str(img_total), str(reel_total), liste