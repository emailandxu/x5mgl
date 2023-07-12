import os
import imgui
import moderngl
import moderngl_window as mglw
from moderngl_window.integrations.imgui import ModernglWindowRenderer

class WindowBase(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL SkinDebugging"
    window_size = (1024, 768)
    aspect_ratio = window_size[0] / window_size[1]
    resizable = True

    resource_dir = os.path.normpath(os.path.join(__file__, '../resources'))

    def __init__(self, ctx: moderngl.Context = None, wnd: "BaseWindow" = None, timer: "BaseTimer" = None, **kwargs):
        super().__init__(ctx, wnd, timer, **kwargs)
        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

    def render(self, time: float, frame_time: float):
        """integrate imgui"""
        self.ctx.clear(0, 0, 0)
        self.ctx.enable(moderngl.DEPTH_TEST)
        imgui.new_frame()
        # super().render(time, frame_time) # may casue not implented error
        self.myrender(time, frame_time)
        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def myrender(self, time, frame_time):
        raise NotImplementedError

    def resource(self, name):
        thepath = os.path.join(self.resource_dir, name)
        assert os.path.exists(thepath)
        return thepath

    def key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

    def resize(self, width: int, height: int):
        self.imgui.resize(width, height)

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

    def unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)


