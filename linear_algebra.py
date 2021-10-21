import math

SANITIZATION_LIMIT = .000001 #Used to convert |values| < this to 0



class Vector:
    def __init__(self, *values):
        self._values = [*values]

    def dimension(self) -> int:
        '''
        Returns the amount of values in the vector, or its dimension.
        '''
        return len(self._values)

    def mag(self) -> float:
        '''
        Returns the magnitude of the vector (square root of the sum of the squares of the individual components).
        '''
        return (sum(i**2 for i in self))**.5

    def onto(self, right: 'Vector') -> 'Vector':
        '''
        Returns the projection of this vector onto a single other vector, right.
        '''
        return ((self*right)/(right*right))*right

    def project(self, *vectors) -> 'Vector':
        '''
        Returns the projection of this vector onto multiple others.
        '''
        vectors = Vector.basis(*vectors)
        return sum(self.onto(v) for v in vectors)

    def sanitize(self):
        '''
        Removes all values close to 0, as defined by SANITIZATION_LIMIT
        '''
        for i in range(len(self)):
            if abs(self[i]) < SANITIZATION_LIMIT: self[i] = 0

    def angle_diff(self, v: 'Vector') -> float:
        '''
        Returns the angle between this vector and v.
        u*v/|u|*|v|
        '''
        return math.acos((self*v)/(self.mag()*v.mag()))

    #Private methods
    pass

    #Static methods
    @staticmethod
    def basis(*vectors) -> ['Vector']:
        '''
        Basis
        '''
        basis = []

        for v in vectors:
            basis.append(v-sum(v.onto(u) for u in basis))

        return basis


    @staticmethod
    def cross(*vectors) -> 'Vector':
        '''
        Returns the cross product of vectors, or the vector perpendicular to all vectors listed.
        '''
        assert vectors[0].dimension() - 1 == len(vectors)
        assert all(vectors[0].dimension() == i.dimension() for i in vectors)


    #Dunder methods
    def __iter__(self):
        return self._values.__iter__()

    def __len__(self):
        '''
        Same as dimension.
        '''
        return len(self._values)

    def __add__(self, right):
        if isinstance(right, Vector): #When right is a vector, add the individual components of the two vectors
            assert self.dimension() == right.dimension()
            return Vector(*(i+j for i,j in zip(self, right)))
        elif type(right) in {int, float}: #When right is a number, add said number to each of the components of this vector
            return Vector(*(i+right for i in self))
        elif type(right) is tuple:
            assert self.dimension() == len(right)
            return Vector(*(i+j for i,j in zip(self, right)))
        else:
            return NotImplemented

    def __radd__(self, left):
        return self + left

    def __sub__(self, right):
        if isinstance(right, Vector): #When right is a vector, subtract the individual components of the two vectors
            assert self.dimension() == right.dimension()
            return Vector(*(i-j for i,j in zip(self, right)))
        elif type(right) in {int, float}: #When right is a number, subtract said number from each of the components of this vector
            return Vector(*(i-right for i in self))
        elif type(right) is tuple:
            assert self.dimension() == len(right)
            return Vector(*(i-j for i,j in zip(self, right)))
        else:
            return NotImplemented

    def __mul__(self, right):
        '''
        When "multiplying" with another Vector, returns the dot product.
        '''
        if isinstance(right, Vector):
            assert self.dimension() == right.dimension()
            return sum(i*j for i,j in zip(self, right))
        elif type(right) in {int, float}: #When right is a number, multiply said number to each of the components of this vector
            return Vector(*(i*right for i in self))
        else:
            return NotImplemented
    
    def __rmul__(self, left):
        return self * left
        
    def __truediv__(self, right):
        if type(right) in {int, float}: #Divide each of the components by right
            return Vector(*(i/right for i in self))
        else:
            return NotImplemented
    
    def __str__(self):
        return '(' + ', '.join(str(i) for i in self) + ')'

    def __repr__(self):
        return f'Vector({", ".join(str(i) for i in self)})'

    def __getitem__(self, index):
        return self._values[index]

    def __setitem__(self, index, value):
        self._values[index] = value




class Matrix:
    def __init__(self, iterable):
        '''
        If the iterable is 2D, the Matrix will deep copy that iterable into its own personal 2D list.
        If the iterable is 1D, the Matrix will initialize as a vertical Matrix ( [1,2,3] => [[1],[2],[3]])
        '''
        self._matrix = []
        for i in iterable:
            if '__iter__' in type(i).__dict__: #2D iterable / This index in the iterable can also be iterated over.
                self._matrix.append([j for j in i]) #Append a list to the matrix which contains all the values of this part of the 2D array.
            else: #1D iterable.
                self._matrix.append([i])
        self._verify()

    def sanitize(self):
        '''
        Changes all values in the Matrix which are near 0 (as defined by SANITIZATION_LIMIT) to 0.
        '''
        for row in range(len(self._matrix)):
            for col in range(len(self._matrix[row])):
                if abs(self._matrix[row][col]) < SANITIZATION_LIMIT: self._matrix[row][col] = 0
                
    def rows(self) -> int:
        return len(self._matrix)

    def columns(self) -> int:
        return len(self._matrix[0])

    def column_vector(self, col: int) -> Vector:
        '''
        Returns the column vector of the given column in the matrix.
        '''
        return Vector(*(i[col] for i in self._matrix))

    def row_vector(self, row: int) -> Vector:
        '''
        Returns the row vector of the given row in the matrix.
        '''
        return Vector(*self[row])

    def transpose(self) -> 'Matrix':
        '''
        Will create a new Matrix which is transposed.
        '''
        return Matrix([[self[col,row] for row in range(self.rows())] for col in range(self.columns())])

    def determinant(self) -> float:
        '''
        Returns the determinant of the matrix.
        Works recursively. Also determines the determinant using the top row, if you care.
        '''
        assert self.square()
        if self.rows() == 1:
            return self[0,0]
        return sum(self[x,0]*self.exclude(x,0).determinant()*(1 if x%2==0 else -1) for x in range(self.columns()))

    def cofactor(self, x: int, y: int) -> float:
        '''
        Returns the cofactor of a given position in the Matrix.
        This is the determinant of the matrix if the given position's row
          and column were completely missing, and also factors in the negative (if the x+y are odd).
        '''
        return self.exclude(x,y).determinant()*(1 if (x+y)%2 == 0 else -1)

    def cofactor_matrix(self) -> 'Matrix':
        '''
        Returns the cofactor matrix of this one, which is just the same
        matrix except each value is replaced by the cofactor of that spot.
        '''
        return Matrix([self.cofactor(x,y) for x in range(self.columns())] for y in range(self.rows()))

    def inverse(self) -> 'Matrix':
        '''
        Returns an inverse of the current matrix, which is 1/determinant
           times the transposed cofactor matrix.
        '''
        assert self.determinant() != 0
        return 1/self.determinant() * self.cofactor_matrix().transpose()

    def exclude(self, col: int, row: int) -> 'Matrix':
        '''
        Returns the matrix, but without the whole col column and row row.
        '''
        return Matrix([self[x,y] for x in range(self.columns()) if x != col] for y in range(self.rows()) if y != row)

    def augment(self, m2) -> 'Matrix':
        '''
        Creates a new matrix which is this Matrix with m2's values added to the right of this matrix. [[1,2,3]] + [[4,5,6]] = [[1,2,3,4,5,6]]
        '''
        assert self.rows() == m2.rows()
        return Matrix([[(self[x,y] if x < self.columns() else m2[x-self.columns(),y]) for x in range(self.columns()+m2.columns())] for y in range(self.rows())])

    def square(self) -> bool:
        '''
        Returns if this matrix is a square matrix
        '''
        return self.rows() == self.columns()

    #Private methods
    def _verify(self):
        '''
        Asserts all the rows have the same length.
        '''
        for row in self:
            assert len(row) == len(self[0])


    #Static Methods
    @staticmethod
    def rotation_matrix(angle: float, axis) -> 'Matrix':
        '''
        Returns the 3D rotation matrix to rotate around the given axis (0, 1, 2 = x, y, z) by angle radians.
        '''
        if axis == 0:
            return Matrix([ [1,                 0,                  0],
                            [0,                 math.cos(angle),    -math.sin(angle)],
                            [0,                 math.sin(angle),    math.cos(angle)]])
        elif axis == 1:
            return Matrix([ [math.cos(angle),   0,                  math.sin(angle)],
                            [0,                 1,                  0],
                            [-math.sin(angle),  0,                  math.cos(angle)]])
        elif axis == 2:
            return Matrix([ [math.cos(angle),   -math.sin(angle),   0],
                            [math.sin(angle),   math.cos(angle),    0],
                            [0,                 0,                  1]])

    #Dunder methods
    def __str__(self):
        return '[' + '\n'.join(', '.join(str(j) for j in i) for i in self._matrix) + ']'

    def __repr__(self):
        return 'Matrix(' + str(self._matrix) + ')'

    def __mul__(self, right):
        if type(right) in {int, float}:
            return Matrix((self[x,y]*right for x in range(len(self._matrix[y]))) for y in range(len(self._matrix)))
        elif isinstance(right, Matrix): #Multiply each value to the value in the equivalent spot in the other matrix
            assert self.columns() == right.columns() and self.rows() == right.rows()
            return Matrix((self[x,y]*right[x,y] for x in range(len(self._matrix[y]))) for y in range(len(self._matrix)))
        elif isinstance(right, Vector): #Do matrix multiplication with the vector
            assert right.dimension() == self.columns()
            return self@Matrix(right)
        else:
            return NotImplemented

    def __rmul__(self, left):
        if isinstance(left, Vector):
            assert left.dimension() == self.rows()
            return Matrix(left).transpose()@self
        return self*left

    def __matmul__(self,right):
        '''
        In case I forget, multiplies the row vectors of this Matrix by
        the column vectors of the other Matrix
        '''
        if isinstance(right, Matrix):
            assert self.columns() == right.rows()
            return Matrix([self.row_vector(row)*right.column_vector(col) for col in range(right.columns())] for row in range(self.rows()))
        elif isinstance(right, Vector):
            assert right.dimension() == self.columns()
            return self@Matrix(right)
        else:
            return NotImplemented

    def __getitem__(self, index):
        '''
        Can do matrix[y][x] or matrix[x,y]. Works with slice notation.
        '''
        if type(index) is slice: #This will return multiple rows (as a new Matrix)
            return Matrix(self._matrix[index])
        elif type(index) is int: #Will return a row, so you can do [y][x]
            return self._matrix[index]
        elif type(index) is tuple: #[x, y], slice notation
            if len(index) != 2: raise TypeError()
            new_matrix = None
            if type(index[1]) is int: new_matrix = [self._matrix[index[1]]]
            elif type(index[1]) is slice: new_matrix = self._matrix[index[1]]
            for row in range(len(new_matrix)):
                if type(index[0]) is int: new_matrix[row] = [new_matrix[row][index[0]]]
                elif type(index[0]) is slice: new_matrix[row] = new_matrix[row][index[0]]
            return Matrix(new_matrix) if (len(new_matrix) != 1 or len(new_matrix[0]) != 1) else new_matrix[0][0]
        else:
            raise TypeError()



if __name__ == '__main__':

    a = Matrix([[1,2,3],
                [4,5,6],
                [7,8,9]])
    assert a[1,2] == 8
    assert a[2][1] == 8

    