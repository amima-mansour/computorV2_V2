import calculation_tools as cal
import errors

def convert_list_string(l):
    string = "[]"
    for key, el in enumerate(l):
        print(el)
        if isinstance(el, list):
            string += convert_list_string(el)
            if key < len(l) - 1:
                string += ";"
        elif el == ',':
            string += ','
        else:
            string+= str(el)
    string += ']'
    return string

# fonction quii permet de verifier que les dimensions de deux matrices sont egales
def compare_dimensions(M1, M2):

    if not isinstance(M1, Matrix) or not isinstance(M2, Matrix):
        errors.check_matrix()
        return "KO"
    try:
        assert M1.col == M2.col
        assert M1.row == M2.row
    except:
        print("Error : Matrix dimensions")
        return "KO"
    return "OK"

# fonction qui permet de verifier que les dimensions de deux matrices sont inversees
def dimensions_multiplication(M1, M2):
    try:
        assert M1.col == M2.row
    except:
        errors.multiplication_matrix()
        return "KO"
    else:
        return "OK"
# fonction qui permet de determiner le determinant de la matrice
def determinant_2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]

def determinant_matrix(M):
    if M.row == 1:
        return M.mat[0][0]
    if M.row == 2:
        return determinant_2(M.mat)
    det = 0
    coeff = 1
    for i in range(n):
        det += coeff * cal.convert_str_nbr(M.mat[i][0]) * determinant_matrix(M.extract(M.mat, i , 0))
        coeff *= -1
    return det 

class Matrix:

    def __init__(self, mat):
        self.mat = mat
        self.row = len(mat)
        self.col = len(mat[0])
        self.det = None

    def matrix_dimensions(self):
        col = 0
        for el in self.m:
            if col == 0:
                col = len(el)
            elif col != len(el):
                return -1
        return col
    
    def print_matrix(self):
        i = 1
        for element in self.mat:
            string = '[ '
            for key, e in enumerate(element):
                if int(e) or not e:
                    e = int(e)
                string += str(e) + ' '
                if key != len(element) - 1:
                    string += ', '
            string += ']'
            print(string)
            i += 1

    # fonction qui permet de verifier que si une matrice est carree
    def square_matrix(self):
            return self.col == self.row

    # fonction qui permet de faire la somme de deux matrices
    def addition(self, M2):
        if compare_dimensions(self, M2) == "KO":
            return None
        M = [[0 for j in range(self.col)] for i in range(self.row)]
        for i in range(self.row):
            for j in range(self.col):
                M[i][j] = cal.convert_str_nbr(self.mat[i][j]) + cal.convert_str_nbr(M2.mat[i][j])
        return Matrix(M)

    # fonction qui permet de faire la soustraction de deux matrices
    def substruction(self, M2):
        if compare_dimensions(self, M2) == "KO":
            return None
        M=[[0 for j in range(self.col)] for i in range(self.row)]
        for i in range(self.row):
            for j in range(self.col):
                M[i][j] = cal.convert_str_nbr(self.mat[i][j]) - cal.convert_str_nbr(M2.mat[i][j])
        return Matrix(M)

    # fonction qui permet de faire la multiplication de deux matrices
    def multiplication(self, M2):
        if dimensions_multiplication(self, M2) == "KO":
            return None
        n1 = self.row
        m1 = M2.col
        M =[[0 for j in range(m1)] for i in range(n1)]#creer une matrice nxn pleine de zéro
        for i in range(n1):
            for j in range(m1):
                for k in range(self.col):
                    M[i][j] += cal.convert_str_nbr(self.mat[i][k]) * cal.convert_str_nbr(M2.mat[k][j])
        return Matrix(M)

    # fonction qui permet de faire la multiplication d'une matrice par un reel
    def multiplication_real(self, real):
        M =[[0 for j in range(self.col)] for i in range(self.row)]#creer une matrice nxn pleine de zéro
        for i in range(self.row):
            for j in range(self.col):
                M[i][j] = real * cal.convert_str_nbr(self.mat[i][j])
        return Matrix(M)

    # fonction qui permet de extraire d'une matrice d'une autre
    def extract(self, line, colunm):
        n = self.row - 1
        M1 =[[0 for j in range(n)] for i in range(n)]
        k = 0
        for i in range(n + 1):
            if i != line: 
                l = 0
                for j in range(n + 1):
                    if j != colunm:
                        M1[k][l] = self.mat[i][j]
                        l += 1
                k += 1
        return Matrix(M1)

    # fonction qui permet de determiner le determinant de la matrice
    def determinant(self):
        if det is None:
            if not self.square_matrix():
                errors.determinant_matrix("This is not a square matrix")
                return None
            self.det = determinant_matrix(self)
            return self.det

    # fonction qui permet de determiner la comatrice
    def comatrice(self):
        comM =[[0 for j in range(self.row)] for i in range(self.col)]#creer une matrice nxn pleine de zéro
        for i in range(self.row):
            for j in range(self.col):
                coeff = (-1) ** (i + j)
                comM[i][j] = coeff * determinant_matrice(extraire_matrice(M, i, j))
        return comM

    # fonction qui permet de determiner la transpose d'une matrice
    def transpose(self):
        transM =[[0 for j in range(self.row)] for i in range(self.col)]#creer une matrice nxn pleine de zéro
        for i in range(self.col):
            for j in range(self.row):
                transM[i][j] = self.mat[j][i]
        return Matrix(transM)

    # fonction qui permet d'inverser une matrice
    def inverse(self):
        if self.det is None:
            self.determinant()
        if self.det is None:
            return None
        if self.det != 0:
            m1 = self.comatrice()
            m1 = m1.transpose()
            return m1.multiplication_real(1 / self.det)
        errors.determinant_matrix("This matrix is not inversible")
        return None
