#!/usr/bin/Python3.4

from sys import exit
import colors

def usage():
    print("Usage : " + colors.red + "./Expert_system.py" + colors.blue + " [-di]" \
            + colors.green + " file.txt" + colors.normal)

def zero_division():
    print(colors.red + "ERROR: Zero Division" + colors.normal)

def brackets():
    print(colors.red + "ERROR: Brakets" + colors.normal)

def syntax():
    print(colors.red + "ERROR: Syntax" + colors.normal)

def var_name(string):
    print(colors.red +  "ERROR: Variable Name\n" + string + " can not be a variable name" + colors.normal)

def operator(c):
    print(colors.red + "ERROR: Operator "+ c + colors.normal)

def unknown_variable(var):
    print(colors.red + "ERROR: This variable "+ var + " is not identified!" + colors.normal)

def wrong_element(msg):
    print(colors.red + "This element " + msg + " is not identified!" + colors.normal)

def error_matrix():
    print(colors.red + "This matrix is not well formated!" + colors.normal)

def function_name(string):
    print(colors.red + "This function name " + string + " is not well formated!" + colors.normal)
