#!/usr/bin/Python3.4

from sys import exit
import colors

def usage():
    print(colors.blue + "Inputs :\n" + colors.red + "Name of variable:" + colors.green + " var = expression\n"+  \
          colors.red + "Name of function:" + colors.green + " f(x) = expression\n"+  \
          colors.red + "Name of matrix:"+ colors.green + " M = expression\n"+  \
          colors.red + "Use ? to know the value of an expression:" + colors.green + " a + b + 2 = ?\n"+  \
          colors.red + "Press matrix to get bonus\n"+  \
          colors.red + "Press exit to quit program"+ colors.normal)

def zero_division():
    print(colors.red + "ERROR: Zero Division" + colors.normal)

def brackets():
    print(colors.red + "ERROR: Brakets" + colors.normal)

def syntax():
    print(colors.red + "ERROR: Syntax" + colors.normal)

def operation():
    print(colors.red + "Operation not permitted!" + colors.normal)

def var_name(string):
    print(colors.red +  "ERROR: Variable Name\n" + string + " can not be a variable name" + colors.normal)

def operator(c):
    print(colors.red + "ERROR: Operator "+ c + colors.normal)

def unknown_variable(var):
    print(colors.red + "ERROR: This variable "+ var + " is not identified!" + colors.normal)

def function(var):
    print(colors.red + "ERROR: This function "+ var + " is not identified!" + colors.normal)

def wrong_element(msg):
    print(colors.red + "This element " + msg + " is not identified!" + colors.normal)

def number():
    print(colors.red + "Number is not well formated!" + colors.normal)


def error_matrix():
    print(colors.red + "This matrix is not well formated!" + colors.normal)

def multiplication_matrix():
    print(colors.red + "Matrix multiplication is not possible!" + colors.normal)

def error_check_matrix():
    print(colors.red + "This expression with matrix is not well formated!" + colors.normal)

def determinant_matrix(string):
    print(colors.red + string + colors.normal)

def cant():
    print(colors.red + "I can't resolve this equation!"+ colors.normal)

def function_name(string):
    print(colors.red + "This function name " + string + " is not well formated!" + colors.normal)
