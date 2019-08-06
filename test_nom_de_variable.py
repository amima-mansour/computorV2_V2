# coding: utf-8

import re

# tester si le nom de la variable est different de i
def test_complexe(chaine):

    try:
        assert chaine != 'i'
        return True
    except:
        print("Error : i can not be the name of a variable")
        return False

# tester si le nom de la fonction est correcte
def test_fonction(chaine):

    motif = r'[a-zA-Z]+\(([a-zA-Z]+\([a-zA-Z]\)|[a-zA-Z])\)'
    try:
        assert re.match(motif, chaine)
        index = chaine.index('(')
        nom_fonction = ''.join(chaine[:index])
        inconnu = chaine[index + 1:index + 2]
        return nom_fonction, inconnu
    except:
        print("Error : it should be like 'f(x)'")
        return "", ""

# tester si le nom de la variable est correcte
def test_variable(chaine):

    motif = r'[a-zA-Z]+'
    try:
        assert re.match(motif, chaine)
        return 1
    except:
        print("Error : variable name is wrong it must be like asd or asD or ASD")
        return 0