#!/usr/bin/Python3.4

import parsing

if __name__ == "__main__":
    string = input()
    p = parsing.Inputs()
    while string != 'exit':
        p.parsing(string)
        print(p.functions)
        string = input()
