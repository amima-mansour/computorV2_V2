import matrix as mat
import RPN_Eval as rpn_eval
import RPN as rpn
import function_tools as func_tools
import calculation_tools as cal

class Function:
    def __init__(self, name, unknown, func_expr):
        self.unknown = unknown
        #self.expr = func_tools.simplify_func(var, unknown)
        self.expr = func_expr
        print("expr = {}".format(func_expr))
        self.name = name

    def evaluate_func(self, var):
        expr = []
        matrix_yes = 0
        for element in self.expr:
            if element == self.unknown:
                expr.append(str(var))
            else:
                expr.append(element)
            if isinstance(element, mat.Matrix):
                matrix_yes = 1
        rp = rpn.shunting(expr)
        if not rp:
            return None
        expr = rp[-1][2].split()
        if matrix_yes:
            return cal.matrix_calculation(expr)
        return rpn_eval.eval_postfix(expr)

    def print_function(self):
        a = False
        for el in self.expr:
            if isinstance(el, mat.Matrix):
                a = True
                break
        if a:
            expr = func_tools.clean_function(self.expr, self.unknown)
            print(func_tools.function_to_str(expr, self.unknown))
        else:
            string = ""
            for i, el in enumerate(self.expr):
                if isinstance(el, mat.Matrix):
                    string += el.str_matrix()
                else:
                    string += el
                if i < len(self.expr) - 1:
                    string += " "
            print(string)
