#!/usr/bin/Python3.4

from sys import exit
import colors

def usage():
    print("Usage : " + colors.red + "./Expert_system.py" + colors.blue + " [-di]" \
            + colors.green + " file.txt" + colors.normal)

def zero_division():
    print(colors.red + "ERROR: Zero Division" + colors.normal)
    exit()

def brackets():
    print(colors.red + "ERROR: Brakets" + colors.normal)

def var_name():
    print(colors.red +  "ERROR: Variable Name" + colors.normal)

def operator(c):
    print(colors.red + "ERROR: Operator" + colors.normal)

def wrong_element(msg):
    print(colors.red + "This element " + msg + " is not identified!" + colors.normal)

def error_matrix():
    print(colors.red + "This matrix is not well formated!" + colors.normal)
