import calculation_tools as calcul
import re
import matrix as mat
import Complex as comp
import parsing
import RPN as rpn
import RPN_Eval as rpn_eval
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

# transfom a function to a list
def convert_func_list(init_list):

    final_list = []
    if '(' not in init_list:
        return init_list
    index_1 = init_list.index('(')
    if index_1 != 0:
        final_list = final_list + transform_list(init_list[:index_1])
    index_1 += 1
    new_list = init_list[index_1:]
    index_2 = index_char(new_list, '(', ')')
    final_list.append(convert_func_list(new_list[:index_2]))
    index_2 += 1
    if index_2 < len(new_list):
        final_list = final_list + convert_func_list(new_list[index_2:])
    return final_list

def transform_list(init_list):

    final_list = []
    # print("init_transform = {}".format(init_list))
    for i, element in enumerate(init_list):
        if element == ')':
            return final_list
        m = re.search(r"(\*|-|%|/|\+|\^)", element)
        if element in '+*-/%^':
            final_list.append(element)
        elif m:
            char = m.group(0)
            inter_list = element.split(char)
            for key, el in enumerate(inter_list):
                if el != '':
                    final_list.append(el)
                if key < len(inter_list) - 1 or (element[- 1] in '+*-/%^' and i < len(element) - 1):
                    final_list.append(char)
        else:
            final_list.append(element)
    return final_list

# # clean a list
def clean_function_list(init_list, final_list, index, unknown):

    if index - 2 >= 0 and init_list[index - 1] == '*':
        final_list.extend(init_list[index-2:index])
    final_list.append(clean_function(init_list[index], unknown))
    index += 1
    if index < len(init_list) and not isinstance(init_list[index], comp.Complex) and init_list  in '*/^':
        final_list.extend(init_list[index:index + 2])
        index += 2
    if index < len(init_list) and init_list[index] in '+-':
        final_list.append(init_list[index])
        index += 1
    return index

# clean a double list
def clean_function(init_list, unknown):

    index = 0
    final_list = []
    while index < len(init_list):
        if isinstance(init_list[index], list) and unknown in init_list[index]:
            index = clean_function_list(init_list, final_list, index, unknown)
            continue
        if init_list[index] == unknown:
            if index - 2 >= 0 and init_list[index - 2] == '0':
                index += 3
                continue
            elif index + 2 < len(init_list) and init_list[index + 2] == '0':
                final_list.extend(init_list[index - 2:index - 1])
            elif index + 2 < len(init_list) and init_list[index + 2] == '1':
                if init_list[index - 2] == '1':
                    final_list.extend(init_list[index:index + 1])
                else:
                    final_list.extend(init_list[index - 2:index + 1])
            elif index - 2 >= 0 and init_list[index - 2] == '1':
                final_list.extend(init_list[index:index + 3])
            else:
                final_list.extend(init_list[index - 2:index + 3])
            if index + 3 < len(init_list) and init_list[index + 3] in '-+':
                final_list.append(init_list[index + 3])
                index += 1
            index += 3
        else:
            index += 1
    return final_list

# simplify function expression : for example 2 * x^2 + 1 + 2 * x + 5 - 2 * x^2 = 2 * x + 6
def simplify_func(list_expr, unknown):

    func_expr = list_expr
    for el in func_expr:
        if isinstance(el, mat.Matrix):
            return func_expr
    expr = func_expr
    dic, final_expr = {}, []
    index, dic[0] = 0, 0
    while index >= 0 and index < len(expr) and len(expr) > 0 :
        print("expr after suppr = {}".format(expr))
        if isinstance(expr[index], list) and unknown in expr[index]:
            if index - 1 >= 0 and expr[index - 1] == '-':
                final_expr.append('-')
            if len(final_expr) > 0 and final_expr[-1] != '-':
                final_expr.append('+')
            if index - 2 >= 0 and expr[index - 1] == '*':
                final_expr.extend(expr[index-2:index])
                del expr[index -2:index]
                index -= 2
            final_expr.append(simplify_func(expr[index], unknown))
            del expr[index]
            if index < len(expr) and (expr[index] == '^' or expr[index] == '/' or expr[index] == '*'):
                final_expr.append(expr[index])
                final_expr.append(simplify_func(expr[index + 1], unknown))
                del expr[index:index + 2]
            if index - 2 >= 0 and expr[index - 1] == '*':
                final_expr.append(expr[index - 2])
                final_expr.append(expr[index - 1])
                #print("expr life = {}".format(expr[index - 2]))
                #final_expr.extend[index-2:index]
            print("expr avant avant = {}".format(final_expr))
            continue
        print(expr)
        if unknown == expr[index]:
            degree, nbr, expr, coeff, index = elements_polynome(expr, index)
            print("expr = {}, nbr = {}".format(expr, nbr))
            if nbr == unknown or expr[index] == '*':
                if nbr == unknown:
                    degree += 1
                    nbr = '1'
                string = expr[index:]
                while index < len(expr) and string[0] == '*':
                    print(index, string[1])
                    if string[1].isdigit():
                        nbr = str(calcul.convert_str_nbr(nbr) * calcul.convert_str_nbr(string[1]))
                    else:
                        degree += 1
                    index += 2
                    string = expr[index:]
                    print("string = {}".format(string))
            if degree in dic.keys():
                if not isinstance(nbr, list) and not isinstance(dic[degree], list):
                    dic[degree] += coeff * calcul.convert_str_nbr(nbr)
            else:
                if not isinstance(nbr, list):
                    dic[degree] = coeff * calcul.convert_str_nbr(nbr)
                else:
                    dic[degree] = nbr
        elif isinstance(expr[index], list):
            p = parsing.Inputs()
            value = p.check_expr("".join(expr[index]), "")
            if not value:
                return None
            rp = rpn.shunting(value)
            var = rpn_eval.eval_postfix(rp[-1][2].split())
            expr[index] = var
            #if index + 1 < len(expr) and expr[index + 1] == '*':
            #    final_expr.append('*')
            #    index += 1
            #del expr[index]
            index += 1
        else:
            index += 1
    tmp = degree_null(expr, unknown)
    if tmp == 'null': return []
    if 0 not in dic:
        dic[0] = str(tmp)
    else:
        dic[0] = str(dic[0]) + str(tmp)
    return final_function(dic, unknown, final_expr)

# find coefficients of degree 0
def degree_null(expr, unknown):

    nbr = 0
    index = 0
    while index < len(expr):
        if type(expr[index]) is not list and (isinstance(expr[index],comp.Complex) or expr[index].isdigit()):
            coeff = 1
            if index == 0:
                if isinstance(expr[index], comp.Complex):
                    nbr = expr[index].str_comp()
                else:
                    nbr = calcul.convert_str_nbr(expr[index])
                index += 1
                continue
            if index - 1 >= 0 and expr[index - 1] in '+-':
                if index - 1 >= 0 and expr[index - 1] == '-':
                    coeff = -1
                nbr += coeff * calcul.convert_str_nbr(expr[index])
        elif isinstance(expr[index], list) and unknown not in expr[index]:
            if nbr != 0 and not isinstance(nbr, list):
                print("Error : mixed types")
                return 'null'
            if not nbr:
                nbr = expr[index]
        else:
            pass
        index += 1
    return nbr

# find the coeff for a degree 
def elements_polynome(expr, index):

    coeff, degree = 1, 1
    # degree
    if index + 2 < len(expr) and expr[index + 1] == '^':
        degree = calcul.convert_str_nbr(expr[index + 2])
        del expr[index + 1: index + 3]
    # nbr
    if index - 2 >= 0 and expr[index - 1] == '*':
        nbr = expr[index - 2]
        del expr[index - 2: index + 1]
        index -= 2
        if index - 1 >= 0 and expr[index - 1] == '-':
            coeff = -1
    elif index + 2 < len(expr) and expr[index + 1] == '*':
        nbr = expr[index + 2]
        del expr[index: index + 3]
        index -= 1
        if index >= 0 and expr[index] == '-':
            coeff = -1
    else:
        if index - 1 >= 0 and expr[index - 1] == '-':
            coeff = -1
        del expr[index]
        index -= 1
        nbr = '1'
    if index < 0: index = 0
    if isinstance(nbr, list):
        print("yes")
    return degree, nbr, expr, coeff, index

# rebuild the function from dictionnary elements
def final_function(dic, unknown, final_list):

    i = 0
    print(dic)
    tmp_list = []
    while len(dic) != 0 :
        if i in dic.keys():
            print(i)
            if i == 0 and len(final_list) != 0:
                tmp_list = [str(dic[i]), '*', unknown, '^', str(i) , '+']
                del dic[i]
                i += 1
                continue
            if len(tmp_list) != 0:
                if dic[i] < 0:
                    tmp_list.append('-')
                    dic[i] *= -1
                else:
                    tmp_list.append('+')
            tmp_list.append(str(dic[i]))
            del dic[i]
        else:
            if i != 0:
                tmp_list.append('+')
            tmp_list.append('0')
        tmp_list.extend(['*', unknown, '^', str(i)])
        i += 1
    if len(final_list) and final_list[0] == '-':
        final_list = tmp_list + final_list
    else:
        final_list = tmp_list + final_list
    print("final_list = {}".format(final_list))
    return final_list

def format(func_string):
    expr = []
    ops = ['+', '-', '/', '%', '*', '^', '(', ')']
    i = 0
    length = len(func_string)
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

# convert function expression from a list to a string
def function_to_str(expr, unknown):

    string = ''
    index = 0
    while index < len(expr):
        if isinstance(expr[index], list):
            if unknown in expr[index]:
                string_inter = function_to_str(expr[index], unknown)
                if unknown not in string_inter:
                    string += string_inter + ' '
                else:
                    string += '(' + string_inter + ')'
        elif isinstance(expr[index], comp.Complex):
            string += expr[index].str_comp()
        else:
            string += expr[index]
        if index != len(expr) - 1:
            if expr[index + 1] == '^' or expr[index] == '^':
                pass
            else:
                string += ' '
        index += 1
    return string

