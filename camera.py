from linear_algebra import Vector
from rotation import Rotation

_DEFAULT_FOCUS = (0,0,-100)

class Camera:
    '''
    Will convert a point in 3D space to a point on a 2D plane.
    Will basically:
        Subtract target vector by location. Location also represents where the focus point screen is.
        Rotate target vector by rotation (inverse)
        Find where on x,y plane the line between the target vector and focus (not the same as location) land
    '''
    def __init__(self, location: Vector = Vector(0,0,-10), focus: Vector = Vector(*_DEFAULT_FOCUS),
                        rotation: Rotation = Rotation(0,0,0)):
        assert location.dimension() == 3
        assert focus.dimension() == 3
        self._loc = location
        self._focus = focus
        self._rot = rotation

    def __call__(self, v: Vector) -> '2D Vector':
        '''
        The brains of the operation B)
        '''
        assert v.dimension() == 3
        trans_v = v - self._loc #Move it relative to the screen's location
        trans_v = self._rot/trans_v #Rotate it (inverse)
        trans_v = trans_v + self._focus

        intersection_finder = trans_v - self._focus #Vector from focus to translated vector
        #Now, intersection is when z=0, and z=0 at -self._focus[z]/intersection_finder[z]
        fraction = (-self._focus[2])/intersection_finder[2]
        return Vector(fraction*intersection_finder[0], fraction*intersection_finder[1])

    def move_focus(self, v: Vector):
        '''
        This will just make the camera look funny - mainly for experimental purposes.
        '''
        self._focus += v

    def move_location(self, v: Vector):
        '''
        This will move where the focus point is in 3D space. (relative to the rotation)
        '''
        v = self._rot*v
        self._loc += v

    def rotate(self, r: Rotation):
        '''
        Rotates the camera, relative to where its currently looking
        '''
        self._rot += r


if __name__ == '__main__':

    c = Camera()

    print(c(Vector(1,1,0))) #Expect (1,1) - assert not working well...

    print(c(Vector(1,1,100))) #(.5,.5)
    print(c(Vector(2,1,100))) #(1,.5)

    

