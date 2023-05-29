import sys
import pygame as pg
import moderngl as mgl
from model import *

class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)) -> None:
        # init pygame module
        pg.init()
        # define window size
        self.WIN_SIZE = win_size
        # set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF) # DOUBLEBUF means that the program will have two buffers. While one is being draw the other is shown and vice versa
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # create object to help track time
        self.clock = pg.time.Clock()
        self.scene = Triangle(self)

    def check_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                sys.exit()
    
    def render(self) -> None:
        # clear frame buffer to a black screen
        self.ctx.clear(0,255,0) 
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()
    
    def run(self) -> None:
        while True:
            self.check_events()
            self.render()
            self.clock.tick(60) # set framerate to 60 fps

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
