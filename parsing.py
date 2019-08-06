#!/usr/bin/Python3.4

import errors
import RPN as rpn

user_input = False

def valid_arg(arg):
    if (len(arg) != 2 and len(arg) != 3) or arg[0] != '-':
        return False
    if arg[1:] != 'd' and arg[1:] != 'i' and arg[1:] != "di" and arg[1:] != "id":
        errors.usage()
    return True

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

    l = []
    ops = ['+', '-', '/', '%', '*', '^', ')', '+']
    if not brackets(string, '(', ')'):
        return False, []
    string = string.replace(" ", "")
    i = 0
    length = len(string)
    while i < length:
        if string[i].isdigit():
            nb = ""
            while i < length and string[i].isdigit():
                nb += string[i]
                i+= 1
            l.append(nb)
            i -= 1
        elif string[i] in ops:
            if i == 0 and string[i] != '-':
                errors.operator(string[i])
                return False, l
            if i == length - 1:
                errors.operator(string[i])
                return False, l
            if i + 1 < length - 1 and string[i + 1] in ops:
                errors.operator(string[i])
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

class Inputs:

    def __init__(self):
        self.variables = dict()
        self.matrixs = dict()
        self.functions = dict()
        self.current = []

    def parsing(self, string):
        'Main function called to read the content of the input'
        if string.count('=') != 1:
            errors.usage()
            return
        string_list = string.split('=')
        var_name = string_list[0].replace(" ", "")
        var_value = string_list[1]
        if var_value == '?':
            self.current = self.check_expr(var_name)
        elif var_name.isalpha():
            if '[' in var_value:
                self.matrixs[var_name.lower()] = self.check_matrix(var_value)
            else:
                self.variables[var_name.lower()] = self.check_expr(var_value)
        elif '(' in var_name:
            func_name, unknown = self.check_function_name(var_name)
            func_expr = self.check_function_expr(var_value, unknown)
            self.functions[func_name] = func_expr
        else:
            errors.var_name()

    def check_expr(self, string):
        value, var_list = check_string(string)
        if not value:
            return value
        rp = rpn.shunting(var_list)
        return rp[-1][2]


    def check_matrix(self, string):
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
                    print(i, string[i])
                    j = i
                    while string[j].isdigit():
                        nb = nb * 10 + int(string[j])
                        j += 1
                    print(string[j])
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

    def check_function_name(self, string):
        return "rien"

    def check_function_expression(self, string, unknown):
        return []
