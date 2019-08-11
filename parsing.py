#!/usr/bin/Python3.4

import errors
import RPN as rpn
import RPN_Eval as rpn_eval
import matrix
import Complex as comp
import function as func
import calculation_tools as cal
import function_tools as func_tools
import check
import matrix as mat

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
                m = check.check_expr_matrix(var_value)
                if m:
                    m = self.replace_var(m, "")
                    m1 = cal.matrix_calculation(m)
                    if m1:
                        self.matrixs[var_name.lower()] = m1
                        m1.print_matrix()
            else:
                value = self.check_expr(var_value, "")
                if not value:
                    return
                a = False
                for el in value:
                    if isinstance(el, list):
                        a = True
                        break
                if not a:
                    rp = rpn.shunting(value)
                    var = rpn_eval.eval_postfix(rp[-1][2].split())
                    self.variables[var_name.lower()] = var
                    var.print_comp()
                else:
                    m1 = cal.matrix_calculation(value)
                    if m1:
                        self.matrixs[var_name.lower()] = m1
                        m1.print_matrix()
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
        for i, el in enumerate(string):
            if isinstance(el, list):
                string[i] = mat.Matrix(string[i])
        value, var_list = check.check_string(string)
        #if not value:
        #    return value
        #rp = rpn.shunting(var_list)
        #return rp[-1][2]
        return None
    
    def check_expr(self, string, ignore):
        value, var_list = check.check_string(string)
        if not value:
            return value
        var_list = self.replace_var(var_list, ignore)
        return var_list

    def replace_var(self, expr, ignore):
        ops = ['+', '-', '/', '%', '*', '^']
        i = 0
        length = len(expr)
        final_expr = []
        while i < length:
            if not isinstance(expr[i], list) and expr[i].isalpha():
                var = expr[i]
                if var.lower() not in self.variables:
                    if var.lower() in self.functions:
                        f = self.functions[var.lower()]
                        if i + 3 < length and expr[i + 1] == '(' and expr[i + 3] == ')':
                            print("var = {}".format(self.functions))
                            nb = expr[i + 2]
                            if nb.isalpha():
                                if nb.lower() in self.variables:
                                    nb = self.variables[nb.lower()]
                                else:
                                    errors.unknown_variable(nb)
                                    return None
                            p = f.evaluate_func(nb)
                            final_expr.append(p)
                            i += 3
                        else:
                            errors.unknown_variable(var)
                    elif var.lower() == ignore or var.lower() == 'i':
                        if len(final_expr) >= 1 and final_expr[-1].isdigit():
                             final_expr += '*'
                        final_expr.append(expr[i])
                    elif var.lower() in self.matrixs:
                        final_expr.append(self.matrixs[var.lower()].mat)
                    else:
                        errors.unknown_variable(var)
                        return None
                else:
                    if len(final_expr) >= 1 and final_expr[-1].isdigit():
                        final_expr += '*'
                    p = self.variables[var.lower()]
                    if p.y != 0:
                        errors.cant("matrix multiplcation with a complexe")
                        return None
                    final_expr.append(str(p.x))
            else:
                final_expr.append(expr[i])
            i += 1
        return final_expr
