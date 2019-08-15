#!/usr/bin/Python3.4

import parsing
import check
import errors
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
                    if not m or (m.isalpha() and m.lower() not in p.matrixs):
                        errors.unknown_variable(m)
                        continue
                    if m.isalpha():
                        mat = p.matrixs[m]
                    else:
                        mat = p.check_expr_matrix(m)
                    if not mat:
                        continue
                    mat = p.matrix_calculation(mat)
                    if func == "det":
                        mat.determinant()
                        if mat.det:
                            print(mat.det)
                    elif func == "inv":
                        m = mat.inverse()
                        if m:
                            print(m.str_matrix('\n'))
                    elif func == "trans":
                        m = mat.transpose()
                        print(m.str_matrix('\n'))
                    else:
                        m = mat.comatrice()
                        print(m.str_matrix('\n'))
        else:
            p.parsing(string)
        string = input()
