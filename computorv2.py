#!/usr/bin/Python3.4

import parsing
import check
import calculation_tools as cal

if __name__ == "__main__":
    string = input()
    func_matrix = ['det', 'inv', 'com', 'trans']
    p = parsing.Inputs()
    while string != 'exit':
        if string == 'matrix':
            while string != 'q':
                print('choose a function from: det, inv, com, trans')
                func = input()
                while func not in func_matrix and func != 'q':
                    print("Error: please choose a function from: det, inv, com, trans and norme or press q")
                    func = input()
                if func == 'q':
                    string = 'q'
                else:
                    print('Put your Matrix')
                    m = input()
                    if m.isalpha():
                        mat = p.matrix[m]
                    else:
                        mat = check.check_matrix(m)
                    if not mat:
                        continue
                    mat = cal.matrix_calculation()
                    if func == "det":
                        mat.determinant()
                    elif func == "inv":
                        mat.inverse()
                    elif func == "trans":
                        mat.transpose()
                    else:
                        mat.comatrice()
        else:
            p.parsing(string)
        string = input()
