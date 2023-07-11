import os
import imgui
import moderngl
import numpy as np
from base import WindowBase


class X5Debugging(WindowBase):
    title = "X5"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def myrender(self, time, frame_time):
        pass

if __name__ == '__main__':
    X5Debugging.run()