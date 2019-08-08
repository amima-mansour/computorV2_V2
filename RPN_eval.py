#!/usr/bin/Python3.4

import errors
import Complex as comp

def eval_postfix(expr):

    print("expr = {}".format(expr))
    ops = ['+', '-', '/', '%', '*', '^']
    stack = []
    for key, token in enumerate(expr):
        if token in ops:
            b = stack.pop()
            if len(stack) == 0 and token == '-':
                a = comp.Complex(0)
                #a rajouter une erreur
            else:
                a = stack.pop()
            if not isinstance(b, comp.Complex):
                b = comp.Complex(b)
            if not isinstance(a, comp.Complex):
                a = comp.Complex(a)
            c = comp.Complex(0)
            c.x = a.x
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

