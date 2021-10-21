from linear_algebra import Vector
from camera import Camera

import pygame

_FPS = 20
_WINDOW_SIZE = (800,500)
_BG_COLOR = pygame.Color(100,100,100)

class ThreeDApp:
    def __init__(self):
        #Camera stuffs
        self._cam = None
        
        #Pygame
        self._running = True
        self._frame = 0
        self._fps = 20
        self._surface = None

        #Example shapes
        self._rectangle = None
        self._rect_color = None



    def run(self) -> None:
        '''
        Runs the pygame program.
        '''

        pygame.init()

        try:
            clock = pygame.time.Clock()

            self._initialize()

            while self._running:
                clock.tick(self._fps)
                self._frame += 1

                self._update_world()
                self._handle_keys()
                self._handle_mouse()

                self._redraw()

        finally:
            pygame.quit()

    def _initialize(self) -> None:
        '''
        Runs everything before the main loop (and after __init__)
        '''
        #Camera Stuffs
        self._cam = Camera()

        #Example shapes
        self._rectangle = [(-50,50,20), (50,50,20),(50,-50,200),(-50,-50,200)]
        self._rect_color = pygame.Color(255,50,50)

        self._resize_display(_WINDOW_SIZE)

    def _update_world(self) -> None:
        '''
        Updates the world once per frame, by checking events and such.        
        '''
        for event in pygame.event.get():
            self._handle_event(event)

    def _handle_event(self, event) -> None:
        '''
        Handles specific events in the pygame.
        '''
        if event.type == pygame.QUIT:
            self._stop_running()
        elif event.type == pygame.VIDEORESIZE:
            self._resize_display(event.size)
        elif event.type == pygame.KEYDOWN:
            pass

    def _handle_keys(self) -> None:
        '''
        Checks which keys are being pressed down and acts on them.
        '''
        keys = pygame.key.get_pressed()

    def _handle_mouse(self) -> None:
        '''
        Handles mouse commands (movement, clicks)
        '''
        mouse = pygame.mouse.get_pressed()
        movement = pygame.mouse.get_rel()

    def _redraw(self) -> None:
        '''
        Draws everything :)
        '''
        #Background color
        pygame.draw.rect(self._surface, _BG_COLOR, 
                                    pygame.Rect(0, 0, self._surface.get_width(),
                                                self._surface.get_height()))

        #Example rectangle
        rect_trans = []
        for vertex in self._rectangle:
            new_v = self._cam(Vector(*vertex))
            rect_trans.append(self._translate_to_origin(new_v))
        
        pygame.draw.polygon(self._surface, self._rect_color, rect_trans)

        pygame.display.flip()

    def _stop_running(self) -> None:
        '''
        Everything which happens at the end of the world
        '''
        self._running = False

    def _resize_display(self, size:(int, int)) -> None:
        '''
        Resizes the display.
        '''
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)

    def _translate_to_origin(self, coordinate, origin = None) -> (float, float):
        '''
        This will flip the image upside down and move the coordinate so its centered around the vertex,
        default being the middle of the window. (Like an x,y plane)
        '''
        if origin == None:
            origin = (self._surface.get_width()/2, self._surface.get_height()/2)
        returning = (coordinate[0]+origin[0], origin[1]-coordinate[1])
        return returning

if __name__ == '__main__':
    ThreeDApp().run()