import matrix as mat
import RPN_Eval as rpn_eval
import RPN as rpn
import function_tools as func_tools
import calculation_tools as cal
import errors

class Function:
    def __init__(self, name, unknown, func_expr):
        self.unknown = unknown
        self.expr = func_expr
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
        string = ""
        for i, el in enumerate(self.expr):
            if isinstance(el, mat.Matrix):
                string += el.str_matrix("")
            else:
                string += el
            if i < len(self.expr) - 1:
                string += " "
        print(string)

    def resolve(self, expr):
        equation = self.expr
        length, i, dic, dic[0] = len(expr), 0, {}, 0
        if 'i' in equation or 'i' in expr or not check_expr(equation, self.unknown) or not check_expr(expr, self.unknown) or not check_matrix(equation) or not check_matrix(expr):
            errors.cant()
            return
        simplify_func(equation, self.unknown, dic, 1)
        simplify_func(expr, self.unknown, dic, -1)
        final_resolve(dic)

def check_expr(equation, unknown):
    tmp = list(equation)
    while '(' in tmp:
        index_open = tmp.index('(')
        index_closed= func_tools.index_char(tmp[index_open + 1:], '(', ')') + index_open
        if unknown in tmp[index_open:index_closed]:
            return False
        del tmp[index_open:index_closed + 1]
    return True

def check_matrix(equation):
    for el in equation:
        if isinstance(el, mat.Matrix):
            return False
    return True

def simplify_func(expr, unknown, dic, mult):

    equation = list(expr)
    index, length, degree = 0, len(equation), 1
    while index < length:
        if equation[index] == unknown:
            equation[index] = '0'
            degree, coeff = 1, 1
            if index - 1 < 0 or equation[index - 1] in '+-':
                nb_1 = 1
                if index - 1 >= 0 and equation[index - 1] == '-':
                    coeff = -1
            else:
                i, nb_1 = index - 2, 1
                if equation[index - 1] == '*':
                    while i >= 0 and equation[i] not in '+-':
                        if equation[i] == ')':
                            opened = 1
                            i -= 1
                            while i >= 0 and opened != 0:
                                if equation[i] == '(':
                                    opened -= 1
                                if equation[i] == ')':
                                    opened += 1
                                i -= 1
                        else:
                            i -= 1
                    string = equation[i + 1:index - 1]
                    rp = rpn.shunting(string)
                    nb = rpn_eval.eval_postfix(rp[-1][2].split())
                    nb_1 = nb.x
                    if i >= 0 and equation[i] == '-':
                        coeff = -1
            if index + 1 < length and equation[index + 1] == '^':
                degree = cal.convert_str_nbr(equation[index + 2])
                index += 2
            j, nb_2 = index + 1, 1
            if index + 1 < length and equation[index + 1] == '*':
                index += 2
                while j < length and equation[j] not in '+-':
                    if equation[j] == '(':
                        opened = 1
                        j += 1
                        while j < length and opened != 0:
                            if equation[j] == ')':
                                opened -= 1
                            if equation[j] == '(':
                                opened += 1
                            j += 1
                        j -= 1
                    else:
                        j += 1
                if equation[index] == '(':
                    index += 1
                string = equation[index:j]
                rp = rpn.shunting(string)
                nb = rpn_eval.eval_postfix(rp[-1][2].split())
                nb_2 = nb.x
                index = j + 1
            nb = nb_2 * nb_1 * mult
            if degree in dic.keys():
                dic[degree] += coeff * nb
            else:
                dic[degree] = coeff * nb
        index += 1
    rp = rpn.shunting(equation)
    nb = rpn_eval.eval_postfix(rp[-1][2].split())
    dic[0] += nb.x * mult


def polynom_degree(dic):

    degree = 0
    for key, el in dic.items():
        if key > degree and el != 0:
            degree = key
    return degree

# resolution
def final_resolve(dic):

    d = polynom_degree(dic)
    if d == 0 and dic[0] == 0:
        print("The solution is:\nAll real numbers")
    elif d == 0 and dic[0] != 0:
        print("The solution is:\nNo possible solution")
    elif d > 2:
        print("The polynomial degree is stricly greater than 2, I can't solve.")
    else:
        a, b, c = 0, 0, 0
        for key, el in dic.items():
            if key == 0:
                c = el
            elif key == 1:
                b = el
            elif key == 2:
                a = el
        if d == 1:
            solution = -1 * c / b
            if type(solution) == float:
                solution = round(solution, 6)
            if not solution:
                solution = 0
            print("The solution is:\n{}".format(solution))
        else:
            solutions(a, b, c)

def solutions(a, b, c):

    discriminant = b ** 2 - 4 * a * c
    if discriminant == 0:
        solution = -1 * b / (2 * a)
        if type(solution) == float:
            solution = round(solution, 6)
        if int(solution) == solution:
            solution = int(solution)
        print ("Discriminant is null, the solution is:\n{}".format(solution))
    elif discriminant > 0:
        root = discriminant ** 0.5
        solution_1 = (-1 * b + root) / (2  * a)
        solution_2 = (-1 * b - root) / (2  * a)
        if type(solution_1) == float:
            solution_1 = round(solution_1, 6)
        if type(solution_2) == float:
            solution_2 = round(solution_2, 6)
        print("Discriminant is strictly positive, the two solutions are:\n{}\n{}".format(solution_2, solution_1))
    else:
        root = (-1 * discriminant) ** 0.5
        first_part = -1 * b / (2 * a)
        second_part =  root / (2  * a)
        if type(first_part) == float:
            first_part = round(first_part, 6)
        if type(second_part) == float:
            second_part = round(second_part, 6)
        print("Discriminant is strictly negative, the two solutions are:\n{} - i * {}\n{} + i * {}".format(first_part,
            second_part, first_part, second_part))
