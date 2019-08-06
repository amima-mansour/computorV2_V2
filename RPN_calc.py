#!/usr/bin/Python3.4

import errors

def eval_postfix(expr):
    """Resolve an equation took in an RPN form.
        Takes the expr <list>"""

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
