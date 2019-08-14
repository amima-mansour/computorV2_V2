
import errors
import Complex as comp

def eval_postfix(expr):

    ops = ['+', '-', '/', '%', '*', '^']
    stack = []
    for key, token in enumerate(expr):
        if token in ops:
            if len(stack) == 0:
                errors.number()
                return None
            b = stack.pop()
            if len(stack) == 0 and token == '-':
                a = comp.Complex(0)
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
                value = c.division_2_complex(b)
                if not value:
                    return None
            elif token == '%':
                c.modulo(b.x)
            else:
                c.multiplication_2_complex(b)
            stack.append(c)
        else:
            stack.append(token)
    c = stack.pop()
    if not isinstance(c, comp.Complex):
        c = comp.Complex(c)
    if int(c.y) == c.y:
        c.y = int(c.y)
    if int(c.x) == c.x:
        c.x = int(c.x)
    return c

