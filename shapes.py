from linear_algebra import Vector
from rotation import Rotation
import math


class BaseObject:

    #Drawing types
    FILL = 0
    OUTLINE = 1
    FILL_OUTLINE = 2
    IMAGE = 3

    def __init__(self, location: Vector = Vector(0,0,0), rotation: Rotation = Rotation(0,0,0)):
        self._loc = location
        self._rot = rotation

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

    def draw(self, camera, higher_movement: [Vector] = list(), higher_rotation: [Rotation] = list()) \
                    -> ['center distance', 'cam location', 'drawing type', 'drawing arguments (ex. list of vectors)']:
        #newpts = mypoints*rotation + location
        #newpts = newpts*higher_rotation + higher_movement
        #cam(newpts)
        pass

    def _translate_pt(self, v: Vector, higher_movement: [Vector] = list(), higher_rotation: [Rotation] = list()) -> Vector:
        '''
        Will translate a point based on this object's location, rotation, and a higher power's location+rotation.
        '''
        new_v = (self._rot*v) + self._loc
        for mov,rot in zip(higher_movement[::-1], higher_rotation[::-1]):
            new_v = (rot*new_v) + mov
        return new_v




class Triangle(BaseObject):
    def __init__(self, v1, v2, v3: Vector, color = None, outline = None, location: Vector = Vector(0,0,0), rotation: Rotation = Rotation(0,0,0)):
        BaseObject.__init__(self, location, rotation)

        self._v1 = v1
        self._v2 = v2
        self._v3 = v3

        self._color = color
        self._outline = outline
        self._draw_type = self.FILL_OUTLINE if (color != None and outline != None) else (self.FILL if (color != None and outline == None) else self.OUTLINE)

    def draw(self, camera, higher_movement: [Vector] = list(), higher_rotation: [Rotation] = list()):
        p1 = self._translate_pt(self._v1, higher_movement, higher_rotation)
        p2 = self._translate_pt(self._v2, higher_movement, higher_rotation)
        p3 = self._translate_pt(self._v3, higher_movement, higher_rotation)

        p1p2 = p2 - p1
        p3p2 = p3 - p2
        normal = Vector.cross(p1p2, p3p2)

        center = (p1+p2+p3)/3
        cam_to_center = camera.focus_to(center)

        angle_diff = normal.angle_diff(cam_to_center)

        cam_p1, p1_loc,z1 = camera(p1)
        cam_p2, p2_loc,z2 = camera(p2)
        cam_p3, p3_loc,z3 = camera(p3)

        new_color = [0,0,0,255]
        new_outline = self._outline
        if self._color != None:
            new_color[0] = self._color[0]*(1-angle_diff/math.pi)
            new_color[1] = self._color[1]*(1-angle_diff/math.pi)
            new_color[2] = self._color[2]*(1-angle_diff/math.pi)
            try:
                new_color[3] = self._color[3]
            except Exception as e:
                new_color[3] = 255

        #cam_to_center.mag()
        return max(z1,z2,z3), max(p1_loc,p2_loc,p3_loc), self._draw_type, [cam_p1, cam_p2, cam_p3], new_color, new_outline
        # draw = dist, cam_loc, draw_type, *draw_args


class Quadrilateral(BaseObject):
    def __init__(self, v1, v2, v3, v4: Vector, color = None, outline = None, location: Vector = Vector(0,0,0), rotation: Rotation = Rotation(0,0,0)):
        BaseObject.__init__(self, location, rotation)

        self._v1 = v1
        self._v2 = v2
        self._v3 = v3
        self._v4 = v4

        self._color = color
        self._outline = outline
        self._draw_type = self.FILL_OUTLINE if (color != None and outline != None) else (self.FILL if (color != None and outline == None) else self.OUTLINE)

    def draw(self, camera, higher_movement: [Vector] = list(), higher_rotation: [Rotation] = list()):
        p1 = self._translate_pt(self._v1, higher_movement, higher_rotation)
        p2 = self._translate_pt(self._v2, higher_movement, higher_rotation)
        p3 = self._translate_pt(self._v3, higher_movement, higher_rotation)
        p4 = self._translate_pt(self._v4, higher_movement, higher_rotation)

        p1p2 = p2 - p1
        p3p2 = p3 - p2
        normal = Vector.cross(p1p2, p3p2)

        center = (p1+p2+p3+p4)/4
        cam_to_center = camera.focus_to(center)

        angle_diff = normal.angle_diff(cam_to_center)

        cam_p1, p1_loc,z1 = camera(p1)
        cam_p2, p2_loc,z2 = camera(p2)
        cam_p3, p3_loc,z3 = camera(p3)
        cam_p4, p4_loc,z4 = camera(p4)

        new_color = [0,0,0,255]
        new_outline = self._outline
        if self._color != None:
            new_color[0] = min(255, max(0, self._color[0]*(1-angle_diff/math.pi)))
            new_color[1] = min(255, max(0, self._color[1]*(1-angle_diff/math.pi)))
            new_color[2] = min(255, max(0, self._color[2]*(1-angle_diff/math.pi)))
            try:
                new_color[3] = self._color[3]
            except Exception as e:
                new_color[3] = 255

        #cam_to_center.mag()
        return max(z1,z2,z3,z4), max(p1_loc,p2_loc,p3_loc,p4_loc), self._draw_type, [cam_p1, cam_p2, cam_p3, cam_p4], new_color, new_outline
        # draw = dist, cam_loc, draw_type, *draw_args