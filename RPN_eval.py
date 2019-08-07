#!/usr/bin/Python3.4

import errors

def eval_complexe_postfix(expr):
    ops = ['-', '/', '%', '*', '^','+']
    expr = expr.split()
    real_stack, img_stack = [], []
    real_img = 0
    for element in expr:
        if element == 'i':
            real_stack.append(0)
        else:
            real_stack.append(element)
    length = len(expr)
    for key, element in enumerate(expr):
        if element in ops:
            if expr[0] == 'i' and expr[1] = 'i':
                if element = '+':
                    img_stack.append(2)
            elif expr[0] == 'i':
            elif expr[1] == 'i':
        



def eval_postfix(expr):

    stack = []
    for token in expr:
        if token == "+":
            a = stack.pop()
            b = stack.pop()
            result = a + b
            stack.append(result)
        elif token == "-":
            a = stack.pop()
            b = stack.pop()
            result = a - b
            stack.append(result)
        elif token == "^":
            a = stack.pop()
            b = stack.pop()
            result = a ** b
            stack.append(result)
        elif token == "/":
            a = stack.pop()
            b = stock.pop()
            if not b:
                errors.zero_division()
            result = a / b
            stack.append(result)
        elif tocken == '%':
            a = stack.pop()
            b = stack.pop()
            if not b:
                errors.zero_division()
            result = a % b
            stack.append(result)
        elif tocken == '*':
            a = stack.pop()
            b = stack.pop()
            result = a * b
            stack.append(result)
        else:
            stack.append(token)
    return stack.pop()

if __name__ == '__main__':
    from sys import argv as av

    if len(av) == 3 and av[1] == "-r":
        expr = list(av[2])
        print(reverse_infix(expr))
    elif len(av) > 1:
        expr = []
        for arg in av[1:]:
            if arg == 'T':
                expr.append(True)
            elif arg == 'F':
                expr.append(False)
            else:
                expr.append(arg)
        print("For input {}".format(expr))
        print("eval_postfix = {}".format(eval_postfix(expr)))
