import errors

# # find the index of closed brackets : char2
def index_char(func_list, char1, char2):

    i = 0
    nbr_char_opened = 1
    longueur = len(func_list)
    while i < longueur:
        if func_list[i] == char1:
            nbr_char_opened += 1
        if func_list[i] == char2:
            nbr_char_opened -= 1
        if nbr_char_opened == 0:
            return i
        i += 1
    return i

def format(func_string):
    expr = []
    ops = ['+', '-', '/', '%', '*', '^', '(', ')']
    length = len(func_string)
    i = 0
    if func_string[0] == '-':
        i = 1
        nb = '-'
        if func_string[1].isdigit():
            while i < length and func_string[i].isdigit():
                nb += func_string[i]
                i +=1
            expr.append(nb)
        elif func_string[1].isalpha():
            nb += "1"
            var = ""
            while i < length and func_string[i].isalpha():
                var += func_string[i]
                i +=1
            expr += [nb, '*', var]
        else:
            errors.operator('-')
            return None
    while i < length:
        if func_string[i] == ' ':
            i += 1
            continue
        if func_string[i] in ops:
            expr.append(func_string[i])
        elif func_string[i].isdigit():
            nb = ""
            while i < length and func_string[i].isdigit():
                nb += func_string[i]
                i +=1
            expr.append(nb)
            continue
        elif func_string[i].isalpha():
            var = ""
            while i < length and func_string[i].isalpha():
                var += func_string[i]
                i +=1
            expr.append(var)
            continue
        elif func_string[i] in "[],;":
            expr.append(func_string[i])
        elif isinstance(func_string[i], list):
            expr += format(func_string[i])
        else:
            errors.operator(func_string[i])
            return None
        i += 1
    return expr
