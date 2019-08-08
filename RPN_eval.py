#!/usr/bin/Python3.4

import errors
import Complex as comp

def eval_postfix(expr):

    ops = ['+', '-', '/', '%', '*', '^']
    stack = []
    c = comp.Complex(0)
    for token in expr:
        if token in ops:
            a = stack.pop()
            b = stack.pop()
            if not isinstance(b, comp.Complex):
                b = comp.Complex(b)
            if not isinstance(a, comp.Complex):
                a = comp.Complex(a)
            c.x  = a.x
            c.y = a.y
            if token == "+":
                c.addition(b)
            elif token == "-":
                c.substruction(b)
            elif token == "^":
                c.power(b.x)
            elif token == "/":
                c.division_2_complex(b)
            elif token == '%':
                c.modulo(b.x)
            else:
                c.multiplication_2_complex(b)
            stack.append(c)
        else:
            stack.append(token)
    return stack.pop()

if __name__ == '__main__':
    from sys import argv as av
    # if len(av) == 3 and av[1] == "-r":
    #     expr = list(av[2])
    #     print(reverse_infix(expr))
    # elif len(av) > 1:
    #     expr = []
    #     for arg in av[1:]:
    #         if arg == 'T':
    #             expr.append(True)
    #         elif arg == 'F':
    #             expr.append(False)
    #         else:
    #             expr.append(arg)
    #     print("For input {}".format(expr))
        # print("eval_postfix = {}".format(eval_postfix(expr)))
