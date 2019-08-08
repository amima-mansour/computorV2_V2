#!/usr/bin/Python3.4
import errors

class Complex:
    def __init__(self, nb):
        self.y = 0 #img
        self.x = 0 #real
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
        self.x = x * comp.x - y * comp.y 
        self.y = x * comp.y + comp.x * y

    def power(self, nbr):
        i = 2
        while i <= nbr:
            multiply_2_complex(self)
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