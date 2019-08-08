#!/usr/bin/Python3.4
import errors

class Complex:
    def __init__(self, nb):
        self.y = 0 #img
        self.x = 0 #real
        print(nb)
        if nb == 'i':
            self.y = 1 
        else:
            self.x = float(nb)
    def module(self):
        return (self.x ** 2 + self.y ** 2)**0.5
    
    def conjugate(self):
        self.y -= self.y

    def multiplication_real(self, nbr):
        self.x *= nbr
        self.y *= nbr

    def multiplication_2_complex(self, comp):
        x = self.x
        y = self.y
        x_1 = comp.x
        y_1 = comp.y
        self.x = x * x_1 - y * y_1 
        self.y = x * y_1 + y * x_1 

    def power(self, nbr):
        i = 2
        if nbr == 0:
            self.y = 0
            self.x = 1
            return
        print("power = {}".format(nbr))
        while i <= nbr:
            self.multiplication_2_complex(self)
            i += 1

    def addition(self, comp):
        self.x += comp.x
        self.y += comp.y
    
    def substruction(self, comp):
        self.x -= comp.x
        self.y -= comp.y

    def division_real(self, nbr):
        if nbr == 0:
            errors.zero_division()
        self.x /= nbr
        self.y /= nbr
    
    def modulo(self, nbr):
        print("modulo = {}".format(nbr))
        if nbr == 0:
            errors.zero_division()
        self.x %= nbr
        self.y %= nbr
    
    def division_2_complex(self, comp):
        if comp.x == 0 and comp.y == 0:
            errors.zero_division()
        module = comp.module()
        conjugate = comp.conjugate()
        self.multiplication_2_complex(conjugate)
        self.division_real(module)
