#!/usr/bin/Python3.4

import errors
import matrix as mat
import function_tools as func_tools

def brackets(s, pushChar, popChar):
    'The function below checks if parentheses are correctly closed'

    stack = []
    for c in s:
        if c == pushChar:
            stack.append(c)
        elif c == popChar:
            if stack == []:
                return False
            else:
                stack.pop()
    return stack == []

def check_string(string):

    ops = ['+', '-', '/', '%', '*', '^', ')', '(']
    ops_2 = ['+', '-', '/', '%', '*', '^','+']
    if not brackets(string, '(', ')'):
        return False, []
    #string = string.replace(" ", "")
    l =[]
    i = 0
    length = len(string)
    while i < length:
        if isinstance(string[i], mat.Matrix):
            l.append(string[i])
        elif string[i].isdigit():
            nb = ""
            while i < length and string[i].isdigit():
                nb += string[i]
                i+= 1
            if i < length and string[i] == '.':
                nb += '.'
                i += 1
                if i == length or not string[i].isdigit():
                    errors.syntax()
                    return False, l
                while i < length and string[i].isdigit():
                    nb += string[i]
                    i+= 1
            l.append(nb)
            i -= 1
        elif string[i] in ops:
            if i == 0 and string[i] not in  '-(':
                errors.operator(string[i])
                return False, l
            if i == length - 1 and string[i] != ')':
                errors.operator(string[i])
                return False, l
            if i + 1 < length and string[i] not in '()' and string[i + 1] in ops_2:
                if string[i + 1] == '*' and string[i] == '*':
                    l.append("**")
                    i += 1
                    if i + 1 < length and string[i + 1] in ops:
                        errors.operator(string[i + 1])
                        return False, l
                    i += 1
                    continue
                else:
                    errors.operator(string[i + 1])
                    return False, l
            if i + 1 < length and string[i] == ')' and string[i + 1] not in ops_2:
                errors.operator(string[i + 1])
                return False, l
            if i + 1 < length and string[i] == '(' and string[i + 1] in ops and string[i + 1] != '-':
                errors.operator(string[i + 1])
                return False, l
            l.append(string[i])
        elif string[i].isalpha():
            var = ""
            while i < length and string[i].isalpha():
                var += string[i]
                i += 1
            i -= 1
            l.append(var)
        else:
            errors.wrong_element(string[i])
            return False, l
        i += 1
    return True, l

def check_expr_matrix(string):
    expr = []
    while len(string) > 0:
        if "[" not in string:
            value, check_expr = check_string(string)
            if not value:
                return None
            else:
                expr += check_expr
                return expr
        index_1 = string.index("[")
        index_2 = func_tools.index_char(string[index_1 + 1:], "[", "]") + index_1 + 1
        tmp_expr = string[:index_1]
        matrix_expr = check_matrix(string[index_1:index_2 + 1])
        if matrix_expr is None:
            return None
        while len(tmp_expr) > 0 and tmp_expr[-1] == ' ':
            tmp_expr = tmp_expr[:-1]
        if len(tmp_expr) > 0:
            if len(tmp_expr) < 2 or ((len(tmp_expr) > 0 and tmp_expr[-1] != '*')):
                errors.error_check_matrix()
                return None
            value, check_expr = check_string(tmp_expr[:-1])
            if not value:
                return None
            expr += check_expr
            expr.append(tmp_expr[-1])
        expr.append(matrix_expr)
        if len(string) > (index_2 + 1):
            while index_2 + 1 < len(string) and string[index_2 + 1] == ' ':
                index_2 += 1
            if len(string) > (index_2 + 1) and string[index_2 + 1] not in '+-*':
                errors.error_check_matrix()
                return None
            char = string[index_2 + 1]
            if index_2 + 2 < len(string) and string[index_2 + 2] in '+*-':
                if string[index_2  +2] != '*' and char != '*':
                    errors.error_check_matrix()
                    return None
                index_2 += 1
                char += '*'
            expr.append(char)
        string = string[index_2 + 2:]
    return expr

def check_matrix(string):
    if not brackets(string, '[', ']'):
        errors.brackets()
        return None
    string = string.strip()
    length = len(string)
    i = 1
    string_list = []
    while i < length - 1:
        if not string[i].isdigit() and string[i] not in ',;[]':
            errors.error_matrix()
            return None
        if string[i] == '[':
            l = []
            i += 1
            while string[i] != "]":
                nb = 0
                j = i
                while string[j].isdigit():
                    nb = nb * 10 + int(string[j])
                    j += 1
                if j != i:
                    i = j
                    l.append(nb)
                else:
                    i += 1
                if not string[i].isdigit() and string[i] not in ',;][':
                    errors.error_matrix()
                    return None
            string_list.append(l)
        i += 1
    if string[-1] != ']' or string[-2] != ']':
        errors.error_matrix()
        return None
    return string_list

def check_function_name(string):
    index_1 = string.index('(')
    index_2 = string.index(')')
    if index_1 == 0 or index_2 != len(string) - 1:
        errors.function_name(string)
        return None, None
    func_name = string[:index_1]
    unknown = string[index_1 + 1: index_2]
    return func_name, unknown
