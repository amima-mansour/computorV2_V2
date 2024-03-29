#!/usr/bin/Python3.4

import errors
import RPN as rpn
import RPN_Eval as rpn_eval
import matrix
import Complex as comp
import function as func
import function_tools as func_tools
import check
import matrix as mat

class Inputs:

    def __init__(self):
        self.variables = dict()
        self.matrixs = dict()
        self.functions = dict()

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
                m = self.check_expr_matrix(var_value)
                if m:
                    m = self.replace_var(m, "")
                    if not m:
                        return
                    m1 = self.matrix_calculation(m)
                    if m1:
                        if var_name != '?':
                            self.matrixs[var_name.lower()] = m1
                        print(m1.str_matrix("\n"))
            else:
                value = self.check_expr(var_value, "")
                if value and value[-1] == '-':
                    errors.operator('-')
                if not value or value[-1] == '-':
                    return
                a = False
                for el in value:
                    if isinstance(el, list):
                        a = True
                        break
                if not a:
                    if '**' in value:
                        errors.operator('**')
                        return
                    rp = rpn.shunting(value)
                    if not rp:
                        return
                    var = rpn_eval.eval_postfix(rp[-1][2].split())
                    if not var:
                        return
                    if var_name != '?':
                        self.variables[var_name.lower()] = var
                    print(var.str_comp())
                else:
                    m1 = self.matrix_calculation(value)
                    if m1:
                        if var_name != '?':
                            self.matrixs[var_name.lower()] = m1
                        print(m1.str_matrix("\n"))
        elif '(' in var_name:
            if var_name.count(')') != 1 or var_name.count(')') != 1:
                errors.function_name(var_name)
                return
            func_name, unknown = check.check_function_name(var_name)
            char = ''
            while var_value[-1] == ' ':
                var_value = var_value[:-1]
            if var_value[-1] == '?':
                char = '?'
                var_value = var_value[:-1]
            if len(var_value) > 0:
                func_expr = func_tools.format(var_value)
            else:
                func_expr = []
            if not func_expr:
                return
            if len(func_expr) > 0:
                func_expr = self.replace_var(func_expr, unknown)
            if not func_expr:
                return
            if len(func_expr) > 0:
                func_expr = self.check_function_expr(func_expr, unknown, var_name)
            if not func_expr:
                return
            if '**' in func_expr:
                errors.operator('**')
                return
            if unknown not in func_expr:
                rp = rpn.shunting(func_expr)
                if not rp:
                    return
                func_expr_2 = rpn_eval.eval_postfix(rp[-1][2].split())
                if not func_expr_2:
                    return
                func_expr = func_expr_2.str_comp()
            if char == '?' and len(func_expr) > 0:
                if func_name.lower() not in self.functions:
                    errors.function(func_name)
                    return
                self.functions[func_name.lower()].resolve(func_expr)
            elif char == '?' and len(func_expr) == 0:
                if func_name.lower() not in self.functions:
                    errors.function(func_name)
                    return
                self.functions[func_name.lower()].print_function()
            else:
                f = func.Function(func_name, unknown, func_expr)
                self.functions[func_name.lower()] = f
                f.print_function()
        else:
            errors.var_name(var_name)

    def check_function_expr(self, string, unknown, var_name):
        if not unknown.isalpha() or len(unknown) != 1:
            errors.function_name(var_name)
            return None
        if not check.brackets(string, '(', ')'):
            errors.brackets()
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

    def check_expr_matrix(self, string):
        expr = []
        while len(string) > 0:
            if "[" not in string:
                value, check_expr = check.check_string(string)
                if not value:
                    return None
                else:
                    expr += check_expr
                    return expr
            index_1 = string.index("[")
            index_2 = func_tools.index_char(string[index_1 + 1:], "[", "]") + index_1 + 1
            tmp_expr = string[:index_1]
            matrix_expr = self.check_matrix(string[index_1:index_2 + 1])
            if matrix_expr is None:
                return None
            while len(tmp_expr) > 0 and tmp_expr[-1] == ' ':
                tmp_expr = tmp_expr[:-1]
            if len(tmp_expr) > 0:
                if len(tmp_expr) < 2:
                    errors.error_check_matrix()
                    return None
                if len(tmp_expr) > 2 and tmp_expr[-1] == '*' and tmp_expr[-2] == '*':
                    value, check_expr = check.check_string(tmp_expr)
                    tmp_expr = tmp_expr.replace(tmp_expr[-2:], "")
                else:
                    value, check_expr = check.check_string(tmp_expr[:-1])
                if not value:
                    return None
                expr += check_expr
                if len(tmp_expr) > 0 and tmp_expr[-1] in '+*-':
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
    
    def check_matrix(self, string):
        if not check.brackets(string, '[', ']'):
            errors.brackets()
            return None
        string = string.strip()
        length = len(string)
        i = 1
        string_list = []
        while i < length - 1:
            if not string[i].isdigit() and string[i] not in ',;[]i+*':
                errors.error_matrix()
                return None
            if string[i] == '[':
                l = []
                i += 1
                last_matrix = ""
                brakets = string[i:].index(']') + i
                if ',' not in string[i:brakets]:
                    errors.error_matrix()
                    return None
                while ',' in string[i:brakets]:
                    comma = string[i:brakets].index(',') + i
                    part_matrix = self.check_expr(string[i:comma], "")
                    if not part_matrix:
                        return None
                    rp = rpn.shunting(part_matrix)
                    if not rp:
                        return None
                    var = rpn_eval.eval_postfix(rp[-1][2].split())
                    if not var:
                        return None
                    l.append(var)
                    i = comma + 1
                last_matrix = self.check_expr(string[i:brakets], "")
                rp = rpn.shunting(last_matrix)
                if not rp:
                    return None
                var = rpn_eval.eval_postfix(rp[-1][2].split())
                if not var:
                    return None
                l.append(var)
                string_list.append(l)
            else:
                errors.error_matrix()
                return None
            i = brakets + 1
            if i < length - 1 and string[i] != ';':
                errors.error_matrix()
                return None
            i += 1
        if string[-1] != ']' or string[-2] != ']':
            errors.error_matrix()
            return None
        length = len(string_list[0])
        for el in string_list:
            if len(el) != length:
                errors.error_matrix()
                return None
        return string_list

    def replace_var(self, expr, ignore):
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
                                if not var:
                                    return None
                                nb = var.str_comp()
                            p = f.evaluate_func(nb)
                            if not p:
                                return None
                            char = '+'
                            if p.y < 0:
                                char = '-'
                            p = '(' + str(p.x) + char + str(p.y) + '*i)'
                            final_expr += p
                            i = index
                        else:
                            errors.unknown_variable(var)
                    elif var.lower() == ignore or var.lower() == 'i':
                        if len(final_expr) >= 1 and not isinstance(final_expr[-1], mat.Matrix)  \
                                and (final_expr[-1].isdigit() or '.' in final_expr[-1]):
                            final_expr += '*'
                        final_expr.append(expr[i])
                    elif var.lower() in self.matrixs:
                        final_expr.append(self.matrixs[var.lower()].mat)
                    else:
                        errors.unknown_variable(var)
                        return None
                else:
                    if len(final_expr) >= 1 and final_expr[-1] not in "*+/%^-(":
                        final_expr += '*'
                    p = self.variables[var.lower()]
                    if p.x == 0 or p.y == 0:
                        if p.x == 0 and p.y == 0:
                            final_expr.append('0')
                        elif p.x == 0:
                            final_expr += ['(', str(p.y), '*', 'i', ')']
                        else:
                            final_expr.append(str(p.x))
                    else:
                        final_expr += ['(', str(p.x), '+', str(p.y), '*', 'i', ')']
            elif expr[i] == '[':
                index = func_tools.index_char("".join(expr[i + 1:]), '[', ']') + i + 1
                m = self.check_matrix("".join(expr[i:index + 1]))
                if not m:
                    return None
                i = index
                final_expr.append(mat.Matrix(m))
            else:
                final_expr.append(expr[i])
            i += 1
        return final_expr

    def matrix_elementary_calculation(self, calc_list, op):
        while op in calc_list:
            a, A, b, B = None, None, None, None 
            index = calc_list.index(op)
            index_2, index_3 = index, index + 1
            if isinstance(calc_list[index - 1], list):
                A = mat.Matrix(calc_list[index - 1])
            elif isinstance(calc_list[index - 1], mat.Matrix):
                A = calc_list[index - 1]
            elif calc_list[index - 1] == ')':
                i = index - 1
                while i > 0 and calc_list[i] != '(':
                    i -= 1
                j = i + 1
                while j < index -1:
                    if isinstance(calc_list[j], comp.Complex):
                        calc_list[j] = str(calc_list[j].x) + " + " + str(calc_list[j].y) + " * i"
                    j += 1
                rp = rpn.shunting(calc_list[i + 1:index-1])
                if not rp:
                    return None
                a = rpn_eval.eval_postfix(rp[-1][2].split())
                if not a:
                    return None
                index_2 = i + 1
            else:
                if not isinstance(calc_list[index - 1], comp.Complex):
                    a = comp.Complex(calc_list[index - 1])
                else:
                    a = calc_list[index - 1]
            if isinstance(calc_list[index + 1], list):
                B = mat.Matrix(calc_list[index + 1])
            elif isinstance(calc_list[index + 1], mat.Matrix):
                B = calc_list[index + 1]
            elif calc_list[index + 1] == '(':
                i = index + 1
                while i < len(calc_list) and calc_list[i] != ')':
                    i += 1
                j = index + 2
                while j < i:
                    if isinstance(calc_list[j], comp.Complex):
                        calc_list[j] = str(calc_list[j].x) + " + " + str(calc_list[j].y) + " * i"
                    j += 1
                rp = rpn.shunting(calc_list[index + 2:i])
                if not rp:
                    return None
                b = rpn_eval.eval_postfix(rp[-1][2].split())
                if not b:
                    return None
                index_3 = i + 1
            else:
                if not isinstance(calc_list[index + 1], comp.Complex):
                    b = comp.Complex(calc_list[index + 1])
                else:
                    b = calc_list[i + 1]
            if op == '**':
                if not A or not B:
                    tmp = None
                    errors.operation()
                else:
                    tmp=  A.multiplication(B)
            elif op == '*':
                if A:
                    tmp = A.multiplication_comp(b)
                elif B:
                    tmp = B.multiplication_comp(a)
                else:
                    a.multiplication_2_complex(b)
                    tmp = a
            elif op == '+':
                if not A or not B:
                    tmp = None
                    errors.operation()
                else:
                    tmp = A.addition(B)
            else:
                if not A or not B:
                    tmp = None
                    errors.operation()
                else:
                    tmp = A.substruction(B)
            if tmp is None:
                return None
            calc_list[index + 1] = tmp
            del calc_list[index + 2:index_3]
            del calc_list[index_2 - 1:index + 1]
        return calc_list

    def matrix_calculation(self, calc_list):
        calc_list = self.matrix_elementary_calculation(calc_list, '**')
        if not calc_list:
            return None
        calc_list = self.matrix_elementary_calculation(calc_list, '*')
        if not calc_list:
            return None
        calc_list = self.matrix_elementary_calculation(calc_list, '-')
        if not calc_list:
            return None
        calc_list = self.matrix_elementary_calculation(calc_list, '+')
        if not calc_list:
            return None
        if not isinstance(calc_list[0], mat.Matrix):
            calc_list[0] = mat.Matrix(calc_list[0])
        return calc_list[0]
