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
        var_value = string_list[1].replace(" ", "")
        if var_value == '?':
            var_name, var_value = var_value, var_name
        if var_name.isalpha() or var_name == '?':
            if var_name == 'i':
                errors.var_name(var_name)
                return
            if '[' in var_value:
                m = check.check_expr_matrix(var_value)
                if m:
                    m = self.replace_var(m, "")
                    m1 = cal.matrix_calculation(m)
                    if m1:
                        if var_name != '?':
                            self.matrixs[var_name.lower()] = m1
                        print(m1.str_matrix())
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
                    if not rp:
                        return
                    print("rp = {}".format(rp[-1][2]))
                    var = rpn_eval.eval_postfix(rp[-1][2].split())
                    if var_name != '?':
                        self.variables[var_name.lower()] = var
                    print(var.str_comp())
                else:
                    m1 = cal.matrix_calculation(value)
                    if m1:
                        if var_name != '?':
                            self.matrixs[var_name.lower()] = m1
                        print(m1.str_matrix())
        elif '(' in var_name:
            if var_name.count(')') != 1 or var_name.count(')') != 1:
                errors.function_name(var_name)
                return
            func_name, unknown = check.check_function_name(var_name)
            func_expr = func_tools.format(var_value)
            if not func_expr:
                return
            func_expr = self.replace_var(func_expr, unknown)
            func_expr = self.check_function_expr(func_expr, unknown, var_name)
            if not func_expr:
                return
            if '**' in func_expr:
                errors.operator('**')
                return
            f = func.Function(func_name, unknown, func_expr)
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
        if not value:
            return None
        return var_list
    
    def check_expr(self, string, ignore):
        string = string.replace(" ", "")
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
                        if i + 3 < length and expr[i + 1] == '(':
                            index = func_tools.index_char(expr[i + 2:], '(', ')') + i + 2
                            nb = "".join(expr[i + 2:index])
                            if nb.isalpha() and nb != 'i':
                                if nb.lower() in self.variables:
                                    nb = self.variables[nb.lower()].str_comp()
                                else:
                                    errors.unknown_variable(nb)
                                    return None
                            else:
                                value = self.check_expr(nb, "")
                                if not value:
                                    return None
                                rp = rpn.shunting(value)
                                if not rp:
                                    return
                                var = rpn_eval.eval_postfix(rp[-1][2].split())
                                nb = var.str_comp()
                            p = f.evaluate_func(nb)
                            final_expr.append(p.str_comp())
                            i = index + 1
                        else:
                            errors.unknown_variable(var)
                    elif var.lower() == ignore or var.lower() == 'i':
                        if len(final_expr) >= 1 and not isinstance(final_expr[-1], mat.Matrix) and final_expr[-1].isdigit():
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
                    final_expr += [str(p.x), '+', str(p.y), '*', 'i']
            elif expr[i] == '[':
                index = func_tools.index_char("".join(expr[i + 1:]), '[', ']') + i + 1
                m = check.check_matrix("".join(expr[i:index + 1]))
                if not m:
                    return None
                i = index
                final_expr.append(mat.Matrix(m))
            else:
                final_expr.append(expr[i])
            i += 1
        return final_expr
