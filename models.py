import shapes
from linear_algebra import Vector
from rotation import Rotation
import math


class Model:

    def __init__(self, *sub_objects, location: Vector = Vector(0,0,0), rotation: Rotation = Rotation(0,0,0)):
        self._loc = location
        self._rot = rotation
        self._objects = [*sub_objects]

    def move(self, movement: Vector):
        '''
        Moves the object's location by just adding it to movement.
        '''
        self._loc += movement

    def move_rotation(self, movement: Vector):
        '''
        Moves the object relative to the object's rotation.
        '''
        self._loc += movement*self._rot

    def rotate(self, rotation: Rotation):
        self._rot += rotation

    def add_object(self, obj):
        self._objects.append(obj)

    def draw(self, camera, higher_movement: [Vector] = list(), higher_rotation: [Rotation] = list()) \
                    -> ['center distance', 'cam location', 'drawing type', 'drawing arguments (ex. list of vectors)']:
        #newpts = mypoints*rotation + location
        #newpts = newpts*higher_rotation + higher_movement
        #cam(newpts)
        #new_move = 

        returning = []

        for o in self._objects:
            if isinstance(o, shapes.BaseObject):
                returning.append(o.draw(camera, higher_movement + [self._loc], higher_rotation + [self._rot]))
            else:
                returning.extend(o.draw(camera, higher_movement + [self._loc], higher_rotation + [self._rot]))

        return returning

    def _translate_pt(self, v: Vector, higher_movement= Vector(0,0,0), higher_rotation = Rotation(0,0,0)) -> Vector:
        '''
        Will translate a point based on this object's location, rotation, and a higher power's location+rotation.
        '''
        new_v = (self._rot*v) + self._loc
        new_v = (higher_rotation*new_v) + higher_movement
        return new_v


class Cube(Model):
    def __init__(self, edge_length, color, location, rotation):
        sub_objs = []
        sub_objs.append(shapes.Quadrilateral(Vector(-edge_length/2,-edge_length/2,0),Vector(edge_length/2,-edge_length/2,0),Vector(edge_length/2,edge_length/2,0),Vector(-edge_length/2,edge_length/2,0),color,location=Vector(0,0,-edge_length/2),rotation=Rotation(0,0,0)))
        sub_objs.append(shapes.Quadrilateral(Vector(-edge_length/2,-edge_length/2,0),Vector(edge_length/2,-edge_length/2,0),Vector(edge_length/2,edge_length/2,0),Vector(-edge_length/2,edge_length/2,0),color,location=Vector(0,0,edge_length/2),rotation=Rotation(0,math.pi,0)))
        sub_objs.append(shapes.Quadrilateral(Vector(-edge_length/2,-edge_length/2,0),Vector(edge_length/2,-edge_length/2,0),Vector(edge_length/2,edge_length/2,0),Vector(-edge_length/2,edge_length/2,0),color,location=Vector(edge_length/2,0,0),rotation=Rotation(0,math.pi/2,0)))
        sub_objs.append(shapes.Quadrilateral(Vector(-edge_length/2,-edge_length/2,0),Vector(edge_length/2,-edge_length/2,0),Vector(edge_length/2,edge_length/2,0),Vector(-edge_length/2,edge_length/2,0),color,location=Vector(-edge_length/2,0,0),rotation=Rotation(0,-math.pi/2,0)))
        sub_objs.append(shapes.Quadrilateral(Vector(-edge_length/2,-edge_length/2,0),Vector(edge_length/2,-edge_length/2,0),Vector(edge_length/2,edge_length/2,0),Vector(-edge_length/2,edge_length/2,0),color,location=Vector(0,edge_length/2,0),rotation=Rotation(-math.pi/2,0,0)))
        sub_objs.append(shapes.Quadrilateral(Vector(-edge_length/2,-edge_length/2,0),Vector(edge_length/2,-edge_length/2,0),Vector(edge_length/2,edge_length/2,0),Vector(-edge_length/2,edge_length/2,0),color,location=Vector(0,-edge_length/2,0),rotation=Rotation(math.pi/2,0,0)))
        Model.__init__(self,*sub_objs,location= location,rotation= rotation)