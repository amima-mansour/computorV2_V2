import errors
def convert_str_nbr(nbr):

    print(nbr)
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