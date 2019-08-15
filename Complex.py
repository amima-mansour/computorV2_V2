import errors

class Complex:
    def __init__(self, nb=0, x=0, y=0):
        self.y = y #img
        self.x = x #real
        if nb == 'i':
            self.y = 1 
        elif nb != 0 and x == 0:
            self.x = float(nb)

    def module(self):
        return (self.x ** 2 + self.y ** 2)
    
    def conjugate(self):
        x = self.x
        y = -1 * self.y
        c = Complex(0, x, y)
        return c

    def multiplication_real(self, nbr):
        self.x *= nbr
        self.y *= nbr

    def multiplication_2_complex(self, comp=None, x_2=0, y_2=0):
        if comp is not None:
            x_1 = comp.x
            y_1 = comp.y
        else:
            x_1 = x_2
            y_1 = y_2
        x = self.x
        y = self.y
        self.x = x * x_1 - y * y_1 
        self.y = x * y_1 + y * x_1

    def power(self, nbr):
        i = 2
        if nbr == 0:
            self.y = 0
            self.x = 1
            return
        x = self.x
        y = self.y
        while i <= nbr:
            self.multiplication_2_complex(None, x, y)
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
            return False
        mod = comp.module()
        conj = comp.conjugate()
        self.multiplication_2_complex(conj)
        self.division_real(mod)
        return True

    def str_comp(self):
        string = ""
        if self.x == self.y and self.y == 0:
            return "0"
        if self.x != 0:
            if int(self.x) == self.x:
                self.x = int(self.x)
            char = ""
            if self.x < 0:
                char = '-'
                self.x *= -1
            string = char + str(self.x)
        y = self.y
        if y != 0:
            if y < 0:
                if self.x == 0:
                    string += "-"
                else:
                    string += " - "
                y *= -1
            else:
                if self.x != 0:
                    string += " + "
            if y > 1:
                if int(y) == y:
                    y = int(y)
                string += str(y)
            string += 'i'
        return string

