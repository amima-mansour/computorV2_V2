#!/usr/bin/Python3.4

import errors
import RPN as rpn
import RPN_Eval as rpn_eval
import matrix
import Complex as comp
import function as func
import function_tools as func_tools
import check

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
                m = check.check_matrix(var_value)
                if m:
                    m1 = matrix.Matrix()
                    if m1.col == -1:
                        errors.matrix()
                        return  
                    self.matrixs[var_name.lower()] = m1 
                    m1.print_matrix()
            else:
                self.variables[var_name.lower()] = rpn_eval.eval_postfix(self.check_expr(var_value, ""))
        elif '(' in var_name:
            if var_name.count(')') != 1 or var_name.count(')') != 1:
                errors.function_name(var_name)
                return
            func_name, unknown = check.check_function_name(var_name)
            func_expr = self.replace_var(func_tools.format(var_value), unknown)
            func_rpn = self.check_function_expr(func_expr, unknown, var_name)
            f = func.Function(func_name, unknown, func_rpn, func_expr)
            self.functions[func_name] = f
            f.print_function()
        else:
            errors.var_name(var_name)

    def check_function_expr(self, string, unknown, var_name):
        if not unknown.isalpha() or len(unknown) != 1:
            errors.function_name(var_name)
            return None
        if not check.brackets(string, '(', ')'):
            errors.check.brackets()
            return None
        value, var_list = check.check_string(" ".join(string))
        if not value:
            return value
        rp = rpn.shunting(var_list)
        return rp[-1][2]
    
    def check_expr(self, string, ignore):
        value, var_list = check.check_string(string)
        if not value:
            return value
        rp = rpn.shunting(var_list)
        value = self.replace_rpn_var(rp[-1][2], ignore)
        return value

    def replace_rpn_var(self, expr, ignore):
        ops = ['+', '-', '/', '%', '*', '^']
        i = 0
        expr = expr.split()
        length = len(expr)
        final_expr = []
        while i < length:
            if expr[i].isalpha():
                var = expr[i]
                if var.lower() == ignore or var.lower() == 'i':
                    final_expr.append(var.lower())
                    if len(final_expr) >= 2 and not isinstance(final_expr[-2], comp.Complex) and final_expr[-2].isdigit():  
                        if (i + 1 < length and (expr[i + 1] not in ops or (expr[i + 1] == '-' and i == 1))) or i + 1 == length or (i - 2 >= 0 and expr[i - 2] not in ops):
                            final_expr += '*'
                elif var.lower() not in self.variables:
                    if var.lower() in self.functions:
                        print("OK")
                        # i += 1
                        # final_expr.append(evaluate_func(self.functions[var.lower()][1], expr[i], self.functions[var.lower()][0]))
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
        return final_expr

    def replace_var(self, expr, ignore):
        ops = ['+', '-', '/', '%', '*', '^']
        i = 0
        length = len(expr)
        final_expr = []
        while i < length:
            if expr[i].isalpha():
                var = expr[i]
                if var.lower() not in self.variables:
                    if var.lower() in self.functions:
                        print("OK")
                        # i += 1
                        # final_expr.append(evaluate_func(self.functions[var.lower()][1], expr[i], self.functions[var.lower()][0]))
                    elif var.lower() == ignore:
                        if len(final_expr) >= 1 and final_expr[-1].isdigit():
                            final_expr += '*'
                        final_expr.append(expr[i])
                    else:
                        errors.unknown_variable(var)
                        return None
                else:
                    if len(final_expr) >= 1 and final_expr[-1].isdigit():
                        final_expr += '*'
                    final_expr.append(self.variables[var.lower()])
            else:
                final_expr.append(expr[i])
            i += 1
        return final_expr