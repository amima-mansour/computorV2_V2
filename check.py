#!/usr/bin/Python3.4

import errors
import matrix as mat
import function_tools as func_tools
import RPN as rpn
import RPN_Eval as rpn_eval

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

def check_function_name(string):
    index_1 = string.index('(')
    index_2 = string.index(')')
    if index_1 == 0 or index_2 != len(string) - 1:
        errors.function_name(string)
        return None, None
    func_name = string[:index_1]
    unknown = string[index_1 + 1: index_2]
    return func_name, unknown
