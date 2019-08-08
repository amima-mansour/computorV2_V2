#!/usr/bin/Python3.4

import errors
import RPN as rpn
import RPN_Eval as rpn_eval
import matrix
import Complex as comp

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
    ops = ['+', '-', '/', '%', '*', '^', ')', '(']
    ops_2 = ['+', '-', '/', '%', '*', '^','+']
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
            if var_name == 'i':
                errors.var_name(var_name)
                return
            if '[' in var_value:
                self.matrixs[var_name.lower()] = self.check_matrix(var_value)
                matrix.print_matrix()
            else:
                self.variables[var_name.lower()] = self.check_expr(var_value, "")
                print("real = {}\nimg = {}".format(self.variables[var_name.lower()].x, self.variables[var_name.lower()].y))
        elif '(' in var_name:
            if var_name.count(')') != 1 or var_name.count(')') != 1:
                errors.function_name(var_name)
                return
            func_name, unknown = self.check_function_name(var_name)
            func_expr = self.check_function_expr(var_value, unknown, var_name)
            self.functions[func_name] = func_expr
        else:
            errors.var_name(var_name)

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

    def check_function_name(self, string):
        index_1 = string.index('(')
        index_2 = string.index(')')
        if index_1 == 0 or index_2 != len(string) - 1:
            errors.function_name(string)
            return None, None
        func_name = string[:index_1]
        unknown = string[index_1 + 1: index_2]
        return func_name, unknown

    def check_function_expr(self, string, unknown, var_name):
        if not unknown.isalpha() or len(unknown) != 1:
            errors.function_name(var_name)
            return None
        if not brackets(string, '(', ')'):
            errors.brackets()
            return None
        return self.check_expr(string, unknown)
    
    def check_expr(self, string, ignore):
        value, var_list = check_string(string)
        if not value:
            return value
        rp = rpn.shunting(var_list)
        value = self.replace_var(rp[-1][2], ignore)
        return rpn_eval.eval_postfix(value)

    def replace_var(self, expr, ignore):
        ops = ['+', '-', '/', '%', '*', '^']
        i = 0
        expr = expr.split()
        length = len(expr)
        final_expr = []
        print("expr replace = {}".format(expr))
        while i < length:
            if expr[i].isalpha():
                var = expr[i]
                if var.lower() == ignore or var.lower() == 'i':
                    final_expr.append(var.lower())
                    if len(final_expr) >= 2 and not isinstance(final_expr[-2], comp.Complex) and final_expr[-2].isdigit():
                        if (i + 1 < length and (expr[i + 1] not in ops or (expr[i + 1] == '-' and i == 1))) or i + 1 == length:
                            final_expr += '*'
                elif var.lower() not in self.variables:
                    if var.lower() is in self.functions:
                        i += 1
                        final_expr.append(evaluate_func(self.functions[var.lower()][1], expr[i], self.functions[var.lower()][0]))
                    else:
                        errors.unknown_variable(var)
                        return None
                else:
                    final_expr.append(self.variables[var.lower()])
                    if len(final_expr) >= 2 and not isinstance(final_expr[-2], comp.Complex) and final_expr[-2].isdigit():
                        if (i + 1 < length and expr[i + 1].isdigit()) or i + 1 == length:
                            final_expr += '*'
            else:
                final_expr.append(expr[i])
            i += 1
        print("final list = {}".format(final_expr))
        return final_expr

    def evaluate_func(func, var):
        expr = []
        for element in func:
            if element == unknown:
                expr.append(var)
            else:
                expr.append(element)
        return rpn_eval.eval_postfix(expr)
