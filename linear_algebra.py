import math

SANITIZATION_LIMIT = .000001 #Used to convert |values| < this to 0



class Vector:
    def __init(self, *values):
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

    def __radd__(self, left):
        return self + left

    def __sub__(self, right):
        if isinstance(right, Vector): #When right is a vector, subtract the individual components of the two vectors
            assert self.dimension() == right.dimension()
            return Vector(*(i-j for i,j in zip(self, right)))
        elif type(right) in {int, float}: #When right is a number, subtract said number from each of the components of this vector
            return Vector(*(i-right for i in self))

    def __mul__(self, right):
        '''
        When "multiplying" with another Vector, returns the dot product.
        '''
        if isinstance(right, vector):
            assert self.dimension() == right.dimension()
            return sum(i*j for i,j in zip(self, right))
        elif type(right) in {int, float}: #When right is a number, multiply said number to each of the components of this vector
            return Vector(*(i*right for i in self))
    
    def __rmul__(self, left):
        return self * left
        
    def __truediv__(self, right):
        if type(right) in {int, float}: #Divide each of the components by right
            return Vector(*(i/right for i in self))
    
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

    def sanitize(self):
        '''
        Changes all values in the Matrix which are near 0 (as defined by SANITIZATION_LIMIT) to 0.
        '''
        for row in range(len(self._matrix)):
            for col in range(len(self._matrix[row])):
                if abs(self._matrix[row][col]) < SANITIZATION_LIMIT: self._matrix[row][col] = 0
                
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