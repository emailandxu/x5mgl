import os
import imgui
import moderngl
import numpy as np
from base import WindowBase
from mathutil import *
from widgets import *
from mesh import Mesh

class X5Debugging(WindowBase):
    title = "X5"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prog = self.load_program("default.glsl")
        self.mesh = Mesh.load(self.resource("bunny/bunny.obj"))
        self.vao = self.mesh.create_vao(self.ctx, self.prog)
        self.w_camera = camera_widget(self.aspect_ratio, )
        self.w_transform = transform_widget("bunny", trans=(0.0, 0, 0), eulers=(0, np.pi/2, 0), scale=(0.5, 0.5, 0.5))

    def myrender(self, time, frame_time):
        proj, view, light_pos = self.w_camera()
        self.prog['proj'].write(proj.astype('f4'))
        self.prog['view'].write(view.astype('f4'))
        self.prog['Light'].value = light_pos
        model = self.w_transform()
        self.prog['model'].write(model.astype('f4'))

        self.vao.render()

if __name__ == '__main__':
    X5Debugging.run()