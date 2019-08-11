import errors
import matrix as mat
import Complex as comp

def convert_str_nbr(nbr):

    if float(nbr):
        return float(nbr)
    return int(nbr)

def elementary_calculation(calc_list, op):

    while op in calc_list:
        index = calc_list.index(op)
        n_1 = convert_str_nbr(calc_list[index - 1])
        n_2 = convert_str_nbr(calc_list[index + 1])
        if op == '^':
            tmp = n_1 ** n_2
        elif op == '*':
            tmp = n_1 * n_2
        elif op == '/' or op == '%':
            if not n_2:
                errors.zero_division()
                return None
            if op == '/':
                tmp = n_1 / n_2
            else:
                tmp = n_1 % n_2
        elif op == '+':
            tmp = n_1 + n_2
        else:
            tmp = n_1 - n_2
        del calc_list[index]
        calc_list[index - 1] = str(tmp)
        del calc_list[index]
    return calc_list

def calculation(calc_list):

    calc_list = elementary_calculation(calc_list, '^')
    calc_list = elementary_calculation(calc_list, '/')
    calc_list = elementary_calculation(calc_list, '%')
    calc_list = elementary_calculation(calc_list, '*')
    calc_list = elementary_calculation(calc_list, '-')
    calc_list = elementary_calculation(calc_list, '+')
    return calc_list[0]

def matrix_elementary_calculation(calc_list, op):

    while op in calc_list:
        a, A, b, B = None, None, None, None
        index = calc_list.index(op)
        if isinstance(calc_list[index - 1], list):
            A = mat.Matrix(calc_list[index - 1])
        elif isinstance(calc_list[index - 1], mat.Matrix):
            A = calc_list[index - 1]
        elif isinstance(calc_list[index - 1], comp.Complex):
            if calc_list[index - 1].y == 0:
                a = calc_list[index - 1].x
            else:
                errors.cant("matrix multiplication with a comlex")
                return None
        else:
            a = float(calc_list[index - 1])
        if isinstance(calc_list[index + 1], list):
            B = mat.Matrix(calc_list[index + 1])
        elif isinstance(calc_list[index + 1], mat.Matrix):
            B = calc_list[index + 1]
        elif isinstance(calc_list[index + 1], comp.Complex):
            if calc_list[index + 1].y == 0:
                b = calc_list[index + 1].x
            else:
                errors.cant("matrix multiplication with a comlex")
                return None
        else:
            b = float(calc_list[index + 1])
        if op == '**':
            if not A or not B:
                tmp = None
            else:
               tmp=  A.multiplication(B)
        elif op == '*':
            if A:
                tmp = A.multiplication_real(b)
            elif B:
                tmp = B.multiplication_real(a)
            else:
                tmp  = a * b
        elif op == '+':
            if not A or not B:
                tmp = None
            else:
                tmp = A.addition(B)
        else:
            if not A or not B:
                tmp = None
            else:
                tmp = A.substruction(B)
        del calc_list[index]
        if tmp is None:
            return None
        calc_list[index - 1] = tmp
        del calc_list[index]
    return calc_list

def matrix_calculation(calc_list):

    calc_list = matrix_elementary_calculation(calc_list, '**')
    if not calc_list:
        return None
    calc_list = matrix_elementary_calculation(calc_list, '*')
    if not calc_list:
        return None
    calc_list = matrix_elementary_calculation(calc_list, '-')
    if not calc_list:
        return None
    calc_list = matrix_elementary_calculation(calc_list, '+')
    if not calc_list:
        return None
    if not isinstance(calc_list[0], mat.Matrix):
        calc_list[0] = mat.Matrix(calc_list[0])
    return calc_list[0]

def evaluate_function(calc_list):

    if len(calc_list) == 1:
        return calc_list[0]
    if len(calc_list) == 2 and calc_list[0] == '-':
        return ('-' + calc_list[1])
    final_list = []
    for i, element in enumerate(calc_list):
        if isinstance(element, list):
            final_list.append(evaluate_function(element))
        else:
            final_list.append(element)
    return calculation(final_list)
