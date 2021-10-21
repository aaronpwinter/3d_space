from linear_algebra import Vector, Matrix


class Rotation:
    '''
    Holds a rotation value for 3D space. In specific, the x, y and z axis
      rotation of something. Will also provide Matricies for rotating
      vectors about its x, y, and z directions. Uses radians.
    Rotation order is the order in which you will rotate around the axises (?),
      defaulting to y -> x -> z
    '''
    def __init__(self, x: float, y: float, z: float, rotation_order: (int) = (1,0,2)):
        self._x = x
        self._y = y
        self._z = z
        self._order = rotation_order

        self._rot_matrix = None
        self._inv_matrix = None
        self._compute_matrices()

    def _compute_matrices(self):
        '''
        Internally computes the rotation matrix using the rotation order.
        '''
        self._rot_matrix = Matrix.rotation_matrix(self[self._order[0]], self._order[0])
        for axis in self._order[1:]:
            self._rot_matrix = self._rot_matrix@Matrix.rotation_matrix(self[axis], axis)
        self._inv_matrix = self._rot_matrix.inverse()


    def __getitem__(self, index):
        '''
        Returns x for 0, y for 1, z for 2 (can also use chars)
        '''
        if index == 0 or index == 'x': return self._x
        if index == 1 or index == 'y': return self._y
        if index == 2 or index == 'z': return self._z

    
    def __mul__(self, right):
        '''
        Only works with vectors, returns the result of rotating the vector
        '''
        return (right*self._rot_matrix).row_vector(0)

    def __truediv__(self, right):
        '''
        Only works with vectors, returns the result of rotating the vector in the inverse way
        '''
        return (right*self._inv_matrix).row_vector(0)



if __name__ == '__main__':
    r = Rotation(1,2,3)

    v = Vector(1,2,3)
    
    v2 = r*v
    print(v2)
    v3 = r/v2
    print(v3)