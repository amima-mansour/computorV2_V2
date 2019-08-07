# coding: utf-8

import parsing
if __name__ == "__main__":
    #chaine = raw_input()
    string = input()
    p = parsing.Inputs()
    while string != 'exit':
        p.parsing(string)
        print(p.variables)
        # chaine = raw_input()
        string = input()
