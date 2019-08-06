# coding: utf-8

import parsing
if __name__ == "__main__":
    chaine = raw_input()
    p = parsing.Inputs()
    while chaine != 'exit':
        p.parsing(chaine)
        print(p.matrixs)
        chaine = raw_input()
