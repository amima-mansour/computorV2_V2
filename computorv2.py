# coding: utf-8

import parsing
if __name__ == "__main__":
    string = input()
    p = parsing.Inputs()
    while string != 'exit':
        p.parsing(string)
        print(p.variables)
        string = input()
