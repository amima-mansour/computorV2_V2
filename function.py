import matrix as mat
import RPN_Eval as rpn_eval
import function_tools as func_tools

class Function:
    def __init__(self, name, unknown, rpn_expr, func_expr):
        self.unknown = unknown
        self.rpn = rpn_expr
        var = func_tools.convert_func_list(func_expr)
        self.expr = func_tools.simplify_func(var, unknown)
        self.name = name

    def evaluate_func(self, var):
        expr = []
        for element in self.rpn:
            if element == self.unknown:
                expr.append(var)
            else:
                expr.append(element)
        return rpn_eval.eval_postfix(expr)

    def develop_power(self, puissance):
        coeff, carc = 1, '+'
        index, final_list = 0, []
        while index < len(self.expr):
            if self.expr[index] == self.unknown:
                final_list.extend([self.expr[index], '^'])
                final_list.append(str(calculs.nombre(self.expr[index + 2])*puissance))
                index += 2
            elif not isinstance(self.expr[index], list) and self.expr[index] in '+-':
                if carc == self.expr[index]:
                    final_list.append('+')
                else:
                    final_list.append('-')
            elif self.expr[index] == '*':
                final_list.append('*')
            else:
                final_list.append(str(calculs.nombre(self.expr[index])**puissance * coeff))
            index += 1
        tmp, index = 2, 0
        if puissance == 2:
            while index < len(self.expr):
                if self.expr[index] == '-':
                    if carc == self.expr[index]:
                        carc = '+'
                    else:
                        carc = '-'
                elif self.expr[index] == self.unknown:
                    index += 2
                elif self.expr[index] in '*+':
                    pass
                else:
                    tmp *= calculs.nombre(self.expr[index])
                index += 1
            if tmp < 0 and carc == '-':
                coeff, carac = -1, '+'
            final_list.extend([carc, str(coeff * tmp), '*',self.unknown, '^', '1'])
        return final_list

    def print_function(self):
        a = False
        for el in self.expr:
            if isinstance(el, mat.Matrix):
                a = True
                break
        if not a:
            expr = func_tools.clean_function(self.expr, self.unknown)
            print(func_tools.function_to_str(expr, self.unknown))
        else:
            for el in self.expr:
                if isinstance(el, mat.Matrix):
                    el.print_matrix()
                else:
                    print(el)
