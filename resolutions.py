import calculation_tools as cal
import RPN as rpn
import RPN_Eval as rpn_eval
import function_tools as func_tools
import errors

def equation_parameter(equation, unknown):

    a, b, c, index, length = 0, 0, 0, 0, len(equation)
    while index < length:
        if equation[index] == unknown:
            coeff = 1
            if index - 1 < 0 or equation[index - 1] in '+-':
                nb = 1
                if index - 2 >= 0 and equation[index - 2] == '-':
                    coeff *= -1
            else:
                i = index
                while i >= 0 and equation[i] not in '+-':
                    i -= 1
                string = equation[i + 1:index]
                if equation[index - 1] == '*':
                    string = equation[i + 1:index - 1]
                rp = rpn.shunting(string)
                nb = rpn_eval.eval_postfix(rp[-1][2].split())
                nb = nb.x
                if equation[i] == '-':
                    coeff *= -1
            if index + 2 < length and index + 1 == '^': 
                if equation[index + 2] == '0':
                    c += coeff * cal.convert_str_nbr(nb)
                elif equation[index + 2] == '1':
                    b += coeff * cal.convert_str_nbr(nb)
                else:
                    a += coeff * cal.convert_str_nbr(nb)
            else:
                b += coeff * cal.convert_str_nbr(nb)
            equation[index] = '0'
        index += 1
    rp = rpn.shunting(equation)
    nb = rpn_eval.eval_postfix(rp[-1][2].split())
    c += nb.x
    return a, b, c

def polynom_degree(equation, unknown):

    degree, index, length = 0, 0, len(equation)

    while index < length:
        if equation[index] == '^':
            nbr = cal.convert_str_nbr(equation[index + 1])
            if degree < nbr:
                degree = nbr
            index += 2
        elif equation[index] == unknown and (index + 1 < length and equation[index + 1] != '^' or index + 1 == length):
            nbr = 1
            if degree < nbr:
                degree = nbr
            index += 1
        else:
            index += 1
    return degree

# resolution
def resolve(equation, unknown):

    tmp_equation = equation
    if 'i' in equation:
        errors.cant()
        return
    while '(' in tmp_equation:
        index_open = tmp_equation.index('(')
        index_closed = func_tools.index_char(tmp_equation[index_open + 1:], '(', ')') + index_open
        if unknown in tmp_equation[index_open:index_closed]:
            errors.cant()
            return
        del tmp_equation[index_open:index_closed + 1]
    d = polynom_degree(equation, unknown)
    if d == 0:
        print("The solution is:\nAll real numbers")
    elif d == -1:
        print("The solution is:\nNo possible solution")
    elif d > 2:
        print("The polynomial degree is stricly greater than 2, I can't solve.")
    else:
        a, b, c = equation_parameter(equation, unknown)
        print("a = {}, b = {}, c = {}".format(a, b, c))
        if d == 1:
            solution = -1 * c / b
            if type(solution) == float:
                solution = round(solution, 6)
            print("The solution is:\n{}".format(solution))
        else:
            solutions(a, b, c)

def solutions(a, b, c):
    # Cette fonction trouve les solutions d'une equation de second degree.

    discriminant = b**2 - 4 * a * c
    if discriminant == 0:
        solution = -1 * b / (2 * a)
        if type(solution) == float:
            solution = round(solution, 6)
        print ("Discriminant is null, the solution is:\n{}".format(solution))
    elif discriminant > 0:
        racine = discriminant**0.5
        solution_1 = (-1 * b + racine) / (2  * a)
        solution_2 = (-1 * b - racine) / (2  * a)
        if type(solution_1) == float:
            solution_1 = round(solution_1, 6)
        if type(solution_2) == float:
            solution_2 = round(solution_2, 6)
        print("Discriminant is strictly positive, the two solutions are:\n{}\n{}".format(solution_2, solution_1))
    else:
        racine = (-1 * discriminant) ** 0.5
        premiere_partie = -1 * b / (2 * a)
        seconde_partie =  racine / (2  * a)
        if type(premiere_partie) == float:
            premiere_partie = round(premiere_partie, 6)
        if type(seconde_partie) == float:
            seconde_partie = round(seconde_partie, 6)
        print("Discriminant is strictly negative, the two solutions are:\n{} - i * {}\n{} + i * {}".format(premiere_partie,
            seconde_partie, premiere_partie, seconde_partie))
